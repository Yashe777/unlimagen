"""
Thread-safe SQLite database for user management
Replaces JSON-based database.py
"""
import sqlite3
import bcrypt
from datetime import datetime
from threading import Lock
import os

class UserDatabase:
    def __init__(self, db_file='users.db'):
        self.db_file = db_file
        self.lock = Lock()
        self.init_db()
    
    def init_db(self):
        """Initialize database and create tables if they don't exist"""
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    plan TEXT DEFAULT 'free',
                    created TEXT NOT NULL,
                    daily_limit INTEGER DEFAULT 10,
                    subscription_id TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_user(self, email, password):
        """Create a new user"""
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                # Check if user exists
                cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
                if cursor.fetchone():
                    conn.close()
                    return False, "Email already exists"
                
                # Insert new user
                cursor.execute('''
                    INSERT INTO users (email, password, plan, created, daily_limit, subscription_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (email, hashed, 'free', datetime.now().isoformat(), 10, None))
                
                conn.commit()
                conn.close()
                
            return True, "Account created"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def verify_user(self, email, password):
        """Verify user credentials"""
        try:
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
                row = cursor.fetchone()
                conn.close()
                
                if not row:
                    return False
                
                stored_hash = row['password'].encode()
                return bcrypt.checkpw(password.encode(), stored_hash)
        except Exception as e:
            print(f"Verify error: {e}")
            return False
    
    def get_user(self, email):
        """Get user data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return {
                'email': row['email'],
                'plan': row['plan'],
                'created': row['created'],
                'daily_limit': row['daily_limit'],
                'subscription_id': row['subscription_id']
            }
        except Exception as e:
            print(f"Get user error: {e}")
            return None
    
    def update_plan(self, email, plan, subscription_id=None):
        """Update user's plan"""
        try:
            # Determine daily limit based on plan
            if plan == 'basic':
                daily_limit = 50
            elif plan == 'pro':
                daily_limit = -1  # unlimited
            elif plan == 'influencer':
                daily_limit = -1  # unlimited for influencers
            else:
                daily_limit = 10
            
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE users 
                    SET plan = ?, subscription_id = ?, daily_limit = ?
                    WHERE email = ?
                ''', (plan, subscription_id, daily_limit, email))
                
                success = cursor.rowcount > 0
                conn.commit()
                conn.close()
                
            return success
        except Exception as e:
            print(f"Update plan error: {e}")
            return False
    
    def get_all_users(self):
        """Get all users (for admin purposes)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT email, plan, created, daily_limit FROM users')
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'email': row['email'],
                'plan': row['plan'],
                'created': row['created'],
                'daily_limit': row['daily_limit']
            } for row in rows]
        except Exception as e:
            print(f"Get all users error: {e}")
            return []
    
    def migrate_from_json(self, json_file='users.json'):
        """Migrate existing users from JSON to SQLite"""
        import json
        
        if not os.path.exists(json_file):
            print("No JSON file to migrate")
            return 0
        
        try:
            with open(json_file, 'r') as f:
                users_data = json.load(f)
            
            migrated = 0
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                for email, user_data in users_data.items():
                    try:
                        cursor.execute('''
                            INSERT OR IGNORE INTO users 
                            (email, password, plan, created, daily_limit, subscription_id)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            email,
                            user_data.get('password', ''),
                            user_data.get('plan', 'free'),
                            user_data.get('created', datetime.now().isoformat()),
                            user_data.get('daily_limit', 10),
                            user_data.get('subscription_id')
                        ))
                        migrated += 1
                    except Exception as e:
                        print(f"Error migrating {email}: {e}")
                
                conn.commit()
                conn.close()
            
            print(f"✅ Migrated {migrated} users from JSON to SQLite")
            return migrated
        except Exception as e:
            print(f"Migration error: {e}")
            return 0

# Create global instance
db = UserDatabase()

# Auto-migrate if JSON file exists
if os.path.exists('users.json'):
    print("🔄 Found existing users.json, migrating to SQLite...")
    count = db.migrate_from_json()
    if count > 0:
        # Backup old file
        import shutil
        backup_file = f'users.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy('users.json', backup_file)
        print(f"✅ Created backup: {backup_file}")
