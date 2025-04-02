import unittest
from unittest.mock import MagicMock, patch
from database import Database
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

class TestDB(unittest.TestCase):

    @patch('database.libsql.connect')
    def set_up(self, mock_connect):
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.db = Database(
            db_url=os.getenv("TEST_DB_URL", "mock_url"),
            db_auth_key=os.getenv("TEST_DB_KEY", "mock_key")
        )
    
    def test_init(self):
        self.assertIsNotNone(self.db.conn)
        self.assertEqual(self.db.db_url, os.getenv("TEST_DB_URL", "mock_url"))
        self.assertEqual(self.db.db_auth_key, os.getenv("TEST_DB_KEY", "mock_key"))
    
    @patch('bcrypt.checkpw', return_value=True)
    def test_check_user_valid(self, mock_checkpw):
        username = "testuser"
        password = "securepassword"
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (hashed_password,) # Simulate user found
        self.db.conn.cursor.return_value = mock_cursor

        self.assertTrue(self.db.check_user(username, password))
    
    def test_check_user_invalid(self):
        username = "testuser"
        password = "wrongpassword"

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None # Simulate user not found
        self.db.conn.cursor.return_value = mock_cursor

        self.assertFalse(self.db.check_user(username, password))

    def test_register_user_existing(self):
        username = "newuser"
        password = "newpassword"

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,) # Simulate existing user
        self.db.conn.cursor.return_value = mock_cursor

        self.assertFalse(self.db.register_user(username, password)) 
    
    # TODO: Add all the queries and create the mock DB

if __name__ == '__main__':
    unittest.main()