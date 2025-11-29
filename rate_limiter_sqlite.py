"""
Thread-safe SQLite-based rate limiter
Replaces JSON-based rate_limiter.py
"""
import sqlite3
from datetime import datetime
from threading import Lock

class RateLimiter:
    def __init__(self, db_file='rate_limit.db'):
        self.db_file = db_file
        self.lock = Lock()
        self.limits = {
            'anonymous': 3,  # 3 per day for non-signed up users
            'free': 10,      # 10 per day for signed up users
            'basic': 50,     # 50 per day
            'pro': -1,       # unlimited
            'influencer': -1 # unlimited for influencers
        }
        self.init_db()
    
    def init_db(self):
        """Initialize database and create tables"""
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create usage table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage (
                    user_key TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0,
                    date TEXT NOT NULL,
                    tier TEXT DEFAULT 'free'
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_user_key(self, ip_address, user_id=None):
        """Get unique key for user"""
        if user_id:
            return f"user_{user_id}"
        return f"ip_{ip_address}"
    
    def check_limit(self, ip_address, user_id=None, tier='free'):
        """Check if user can generate"""
        key = self.get_user_key(ip_address, user_id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get or create user record
            cursor.execute('SELECT * FROM usage WHERE user_key = ?', (key,))
            row = cursor.fetchone()
            
            if not row or row['date'] != today:
                # New day or new user - reset
                cursor.execute('''
                    INSERT OR REPLACE INTO usage (user_key, count, date, tier)
                    VALUES (?, 0, ?, ?)
                ''', (key, today, tier))
                conn.commit()
                current_count = 0
            else:
                # Update tier
                if row['tier'] != tier:
                    cursor.execute('''
                        UPDATE usage SET tier = ? WHERE user_key = ?
                    ''', (tier, key))
                    conn.commit()
                current_count = row['count']
            
            conn.close()
        
        # Check limit
        limit = self.limits.get(tier, 10)
        if limit == -1:  # unlimited
            return True, -1
        
        remaining = limit - current_count
        return current_count < limit, remaining
    
    def increment(self, ip_address, user_id=None):
        """Increment usage count"""
        key = self.get_user_key(ip_address, user_id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get current record
            cursor.execute('SELECT * FROM usage WHERE user_key = ?', (key,))
            row = cursor.fetchone()
            
            if not row:
                # Create new record
                cursor.execute('''
                    INSERT INTO usage (user_key, count, date, tier)
                    VALUES (?, 1, ?, 'free')
                ''', (key, today))
            elif row['date'] != today:
                # New day - reset count
                cursor.execute('''
                    UPDATE usage SET count = 1, date = ? WHERE user_key = ?
                ''', (today, key))
            else:
                # Increment count
                cursor.execute('''
                    UPDATE usage SET count = count + 1 WHERE user_key = ?
                ''', (key,))
            
            conn.commit()
            conn.close()
    
    def get_usage(self, ip_address, user_id=None):
        """Get current usage count"""
        key = self.get_user_key(ip_address, user_id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT count, date FROM usage WHERE user_key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        
        if not row or row['date'] != today:
            return 0
        
        return row['count']
    
    def migrate_from_json(self, json_file='usage_data.json'):
        """Migrate existing usage data from JSON to SQLite"""
        import json
        import os
        
        if not os.path.exists(json_file):
            print("No usage JSON file to migrate")
            return 0
        
        try:
            with open(json_file, 'r') as f:
                usage_data = json.load(f)
            
            migrated = 0
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                for user_key, data in usage_data.items():
                    try:
                        cursor.execute('''
                            INSERT OR REPLACE INTO usage (user_key, count, date, tier)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            user_key,
                            data.get('count', 0),
                            data.get('date', datetime.now().strftime('%Y-%m-%d')),
                            data.get('tier', 'free')
                        ))
                        migrated += 1
                    except Exception as e:
                        print(f"Error migrating {user_key}: {e}")
                
                conn.commit()
                conn.close()
            
            print(f"✅ Migrated {migrated} usage records from JSON to SQLite")
            return migrated
        except Exception as e:
            print(f"Migration error: {e}")
            return 0

# Create global instance
rate_limiter = RateLimiter()

# Auto-migrate if JSON file exists
import os
if os.path.exists('usage_data.json'):
    print("🔄 Found existing usage_data.json, migrating to SQLite...")
    count = rate_limiter.migrate_from_json()
    if count > 0:
        import shutil
        from datetime import datetime
        backup_file = f'usage_data.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy('usage_data.json', backup_file)
        print(f"✅ Created backup: {backup_file}")
