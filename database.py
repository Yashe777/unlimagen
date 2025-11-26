"""
Simple user database using JSON
"""
import json
import os
from datetime import datetime
import bcrypt

class UserDatabase:
    def __init__(self):
        self.file = 'users.json'
        self.load()
    
    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def create_user(self, email, password):
        if email in self.users:
            return False, "Email already exists"
        
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        self.users[email] = {
            'email': email,
            'password': hashed,
            'plan': 'free',
            'created': datetime.now().isoformat(),
            'daily_limit': 10,
            'subscription_id': None
        }
        self.save()
        return True, "Account created"
    
    def verify_user(self, email, password):
        if email not in self.users:
            return False
        
        stored_hash = self.users[email]['password'].encode()
        return bcrypt.checkpw(password.encode(), stored_hash)
    
    def get_user(self, email):
        return self.users.get(email)
    
    def update_plan(self, email, plan, subscription_id=None):
        if email in self.users:
            self.users[email]['plan'] = plan
            self.users[email]['subscription_id'] = subscription_id
            
            if plan == 'basic':
                self.users[email]['daily_limit'] = 50
            elif plan == 'pro':
                self.users[email]['daily_limit'] = -1
            else:
                self.users[email]['daily_limit'] = 10
            
            self.save()
            return True
        return False

db = UserDatabase()
