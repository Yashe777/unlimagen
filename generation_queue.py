"""
Request queue system to prevent API overload
Limits concurrent AI generation requests
"""
import queue
import threading
import time
from datetime import datetime
import uuid

class GenerationQueue:
    def __init__(self, max_workers=5):
        """
        Initialize queue with limited concurrent workers
        max_workers: Maximum number of concurrent AI API calls (default: 5)
        """
        self.max_workers = max_workers
        self.queue = queue.Queue()
        self.results = {}  # Store results by job_id
        self.lock = threading.Lock()
        self.workers = []
        self.running = True
        
        # Start worker threads
        for i in range(max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
        
        print(f"✅ Generation queue started with {max_workers} workers")
    
    def _worker(self):
        """Worker thread that processes generation requests"""
        while self.running:
            try:
                # Get job from queue (timeout to check running flag)
                job = self.queue.get(timeout=1)
                
                if job is None:
                    break
                
                job_id = job['id']
                generate_func = job['function']
                args = job['args']
                kwargs = job['kwargs']
                
                print(f"🎨 [Worker] Processing job {job_id[:8]}...")
                
                try:
                    # Execute generation function
                    start_time = time.time()
                    result = generate_func(*args, **kwargs)
                    elapsed = time.time() - start_time
                    
                    # Store result
                    with self.lock:
                        self.results[job_id] = {
                            'status': 'completed',
                            'result': result,
                            'error': None,
                            'elapsed': elapsed,
                            'completed_at': datetime.now().isoformat()
                        }
                    
                    print(f"✅ [Worker] Job {job_id[:8]} completed in {elapsed:.2f}s")
                    
                except Exception as e:
                    # Store error
                    with self.lock:
                        self.results[job_id] = {
                            'status': 'failed',
                            'result': None,
                            'error': str(e),
                            'elapsed': time.time() - start_time,
                            'completed_at': datetime.now().isoformat()
                        }
                    
                    print(f"❌ [Worker] Job {job_id[:8]} failed: {str(e)}")
                
                finally:
                    self.queue.task_done()
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Worker error: {e}")
    
    def submit(self, generate_func, *args, **kwargs):
        """
        Submit a generation job to the queue
        Returns job_id for tracking
        """
        job_id = str(uuid.uuid4())
        
        job = {
            'id': job_id,
            'function': generate_func,
            'args': args,
            'kwargs': kwargs,
            'submitted_at': datetime.now().isoformat()
        }
        
        # Initialize result as pending
        with self.lock:
            self.results[job_id] = {
                'status': 'pending',
                'result': None,
                'error': None,
                'queue_position': self.queue.qsize() + 1
            }
        
        # Add to queue
        self.queue.put(job)
        
        print(f"📥 [Queue] Job {job_id[:8]} submitted (queue size: {self.queue.qsize()})")
        
        return job_id
    
    def get_result(self, job_id, timeout=120):
        """
        Wait for and get result of a job
        Returns (success, result_or_error)
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            with self.lock:
                if job_id in self.results:
                    result_data = self.results[job_id]
                    
                    if result_data['status'] == 'completed':
                        # Clean up old result after retrieval
                        del self.results[job_id]
                        return True, result_data['result']
                    
                    elif result_data['status'] == 'failed':
                        error = result_data['error']
                        del self.results[job_id]
                        return False, error
                    
                    # Still pending
            
            time.sleep(0.5)  # Check every 500ms
        
        # Timeout
        with self.lock:
            if job_id in self.results:
                del self.results[job_id]
        
        return False, "Generation timed out after 120 seconds"
    
    def get_status(self, job_id):
        """Get current status of a job"""
        with self.lock:
            if job_id in self.results:
                return self.results[job_id]
        return None
    
    def get_queue_size(self):
        """Get current queue size"""
        return self.queue.qsize()
    
    def shutdown(self):
        """Gracefully shutdown the queue"""
        print("🛑 Shutting down generation queue...")
        self.running = False
        
        # Add None to queue for each worker to signal shutdown
        for _ in range(self.max_workers):
            self.queue.put(None)
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
        
        print("✅ Generation queue shut down")

# Create global queue instance
# Limit to 5 concurrent AI API calls to prevent rate limiting
generation_queue = GenerationQueue(max_workers=5)
