import libsql_experimental as libsql
import pandas as pd
import bcrypt

class Database:
    """
    Class for interacting with the database
    """
    def __init__(self, db_url, db_auth_key):
        """
        Initialization of the database
        """
        self.token = token
        self.db_url = db_url
        self.db_auth_key = db_auth_key

        if (self.db_url is None) or (self.db_auth_key is None):
            raise ValueError("DB_URL and DB_KEY must be set as environment variables")
        self.conn = None

        self.connect_to_db()

    def connect_to_db(self):
        """
        Function to connect to the DB and make it ready to receive queries
        """
        self.conn = libsql.connect(
                "my_db.db",
                sync_url=self.db_url,
                auth_token=self.db_auth_key)

        self.conn.sync()

    def check_user(self, username : str, password : str) -> bool:
        """
        Function to authorize a user and connect them to the right programs.
        Returns True if authentication is successful, otherwise False.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result is None:
                return False
            
            stored_hash = result[0]

            return bcrypt.checkpw(
                    password=password.encode(),
                    hashed_password=stored_hash.encode())
        
        except Exception as e:
            print(f"Database error: {e}")
            return False 
        
    def register_user(self, username : str, password : str) -> bool:
        """
        Function to register a new user and register data on the DB
        """
        try:
            cursor = self.conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("Username already existing on DB")
                return False
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Insert into DB
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password.decode()))
            self.conn.commit()

            return True

        except Exception as e:
            print(f"Database error: {e}")
            return False

    # TODO: Implement other functions to interact with the DB