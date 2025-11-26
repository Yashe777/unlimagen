"""
Simple rate limiter for free tier
"""
from datetime import datetime, timedelta
import json
import os

class RateLimiter:
    def __init__(self):
        self.storage_file = 'usage_data.json'
        self.limits = {
            'free': 10,      # 10 per day
            'basic': 50,     # 50 per day
            'pro': -1        # unlimited
        }
        self.load_data()
    
    def load_data(self):
        """Load usage data from file"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}
    
    def save_data(self):
        """Save usage data to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.data, f)
    
    def get_user_key(self, ip_address, user_id=None):
        """Get unique key for user (IP or user_id)"""
        if user_id:
            return f"user_{user_id}"
        return f"ip_{ip_address}"
    
    def check_limit(self, ip_address, user_id=None, tier='free'):
        """Check if user can generate"""
        key = self.get_user_key(ip_address, user_id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Initialize user data
        if key not in self.data:
            self.data[key] = {'count': 0, 'date': today, 'tier': tier}
        
        # Reset if new day
        if self.data[key]['date'] != today:
            self.data[key] = {'count': 0, 'date': today, 'tier': tier}
        
        # Update tier
        self.data[key]['tier'] = tier
        
        # Check limit
        limit = self.limits.get(tier, 10)
        if limit == -1:  # unlimited
            return True, -1
        
        current_count = self.data[key]['count']
        remaining = limit - current_count
        
        return current_count < limit, remaining
    
    def increment(self, ip_address, user_id=None):
        """Increment usage count"""
        key = self.get_user_key(ip_address, user_id)
        if key in self.data:
            self.data[key]['count'] += 1
            self.save_data()
    
    def get_usage(self, ip_address, user_id=None):
        """Get current usage"""
        key = self.get_user_key(ip_address, user_id)
        if key not in self.data:
            return 0
        return self.data[key]['count']

rate_limiter = RateLimiter()
