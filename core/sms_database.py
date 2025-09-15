"""
SMS Database Models for Flatopia
Handles user sessions and conversation data for SMS interactions
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class SMSDatabase:
    """SMS Database manager for user sessions and conversation data"""
    
    def __init__(self, db_path: str = "sms_sessions.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    phone_number TEXT PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    nationality TEXT,
                    education_level TEXT,
                    field_of_interest TEXT,
                    english_test_status TEXT,
                    budget_range TEXT,
                    priorities TEXT,
                    country_interest TEXT,
                    current_stage TEXT DEFAULT 'greeting',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Conversation history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT,
                    message_type TEXT,  -- 'user' or 'bot'
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (phone_number) REFERENCES user_sessions (phone_number)
                )
            """)
            
            # User choices table (for tracking selections)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_choices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT,
                    stage TEXT,
                    choice_value TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (phone_number) REFERENCES user_sessions (phone_number)
                )
            """)
            
            # Recommendations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT,
                    country_code TEXT,
                    university_name TEXT,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (phone_number) REFERENCES user_sessions (phone_number)
                )
            """)
            
            conn.commit()
    
    def get_user_session(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get user session data"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_sessions WHERE phone_number = ?
            """, (phone_number,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create_user_session(self, phone_number: str) -> Dict[str, Any]:
        """Create new user session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_sessions 
                (phone_number, current_stage, created_at, last_active, status)
                VALUES (?, 'greeting', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'active')
            """, (phone_number,))
            conn.commit()
            return self.get_user_session(phone_number)
    
    def update_user_session(self, phone_number: str, updates: Dict[str, Any]) -> bool:
        """Update user session data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build update query
                set_clauses = []
                values = []
                for key, value in updates.items():
                    if key in ['name', 'age', 'nationality', 'education_level', 
                              'field_of_interest', 'english_test_status', 
                              'budget_range', 'priorities', 'country_interest', 
                              'current_stage']:
                        set_clauses.append(f"{key} = ?")
                        values.append(value)
                
                if set_clauses:
                    set_clauses.append("last_active = CURRENT_TIMESTAMP")
                    values.append(phone_number)
                    
                    query = f"UPDATE user_sessions SET {', '.join(set_clauses)} WHERE phone_number = ?"
                    cursor.execute(query, values)
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Error updating user session: {e}")
            return False
    
    def add_conversation_message(self, phone_number: str, message_type: str, content: str) -> bool:
        """Add message to conversation history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversation_history (phone_number, message_type, content)
                    VALUES (?, ?, ?)
                """, (phone_number, message_type, content))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding conversation message: {e}")
            return False
    
    def add_user_choice(self, phone_number: str, stage: str, choice_value: str) -> bool:
        """Record user choice"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_choices (phone_number, stage, choice_value)
                    VALUES (?, ?, ?)
                """, (phone_number, stage, choice_value))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding user choice: {e}")
            return False
    
    def add_recommendation(self, phone_number: str, country_code: str, 
                          university_name: str, details: str) -> bool:
        """Add recommendation for user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO recommendations (phone_number, country_code, university_name, details)
                    VALUES (?, ?, ?, ?)
                """, (phone_number, country_code, university_name, details))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding recommendation: {e}")
            return False
    
    def get_conversation_history(self, phone_number: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM conversation_history 
                WHERE phone_number = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (phone_number, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def cleanup_old_data(self):
        """Clean up data older than 12 months"""
        try:
            cutoff_date = datetime.now() - timedelta(days=365)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean up old sessions
                cursor.execute("""
                    DELETE FROM user_sessions 
                    WHERE last_active < ?
                """, (cutoff_date,))
                
                # Clean up old conversation history
                cursor.execute("""
                    DELETE FROM conversation_history 
                    WHERE timestamp < ?
                """, (cutoff_date,))
                
                # Clean up old choices
                cursor.execute("""
                    DELETE FROM user_choices 
                    WHERE timestamp < ?
                """, (cutoff_date,))
                
                # Clean up old recommendations
                cursor.execute("""
                    DELETE FROM recommendations 
                    WHERE created_at < ?
                """, (cutoff_date,))
                
                conn.commit()
                logger.info("Cleaned up old data")
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")

# Global database instance
sms_db = SMSDatabase()