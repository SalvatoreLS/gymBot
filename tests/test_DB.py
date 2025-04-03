import unittest
from unittest.mock import MagicMock, patch
from src.database import Database
import bcrypt
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

load_dotenv()

class TestDB(unittest.TestCase):

    @patch('database.libsql.connect')
    def setUp(self, mock_connect):
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
    
    def test_connect_to_db(self):
        self.db.connect_to_db()
        self.mock_conn.sync.assert_called_once()
        self.mock_conn.cursor.assert_called_once()
        self.mock_conn.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()
        self.mock_conn.close.assert_called_once()
        self.assertIsNotNone(self.db.conn)
        self.assertEqual(self.db.conn, self.mock_conn)
    
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