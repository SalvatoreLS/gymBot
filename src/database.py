import psycopg2
import pandas as pd
import bcrypt

from pandas.errors import DatabaseError
class Database:
    """
    Class for interacting with the database
    """
    def __init__(self, db_host, db_password, db_user, db_name, db_port):
        """
        Initialization of the database
        """
        self.db_host = db_host
        self.db_password = db_password
        self.db_user = db_user
        self.db_name = db_name
        self.db_port = db_port

        self.conn = None
        self.cursor = None

        if self.db_host is None or self.db_password is None or self.db_user is None or self.db_name is None or self.db_port is None:
            raise ValueError("Error with the DB connection parameters")

        self.connect_to_db()

    def connect_to_db(self):
        """
        Function to connect to the DB and make it ready to receive queries
        """
        self.conn = psycopg2.connect(
            host=self.db_host,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port
        )

        if self.conn is None:
            raise DatabaseError("self.conn is None. Error with the DB")
        
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT version();")
        db_version = self.cursor.fetchone()
        print(f"Connected to database: {self.db_name} on {self.db_host} with version: {db_version[0]}")
        self.conn.commit()

    def check_user(self, username : str, password : str) -> int:
        """
        Function to authorize a user and connect them to the right programs.
        Returns True if authentication is successful, otherwise False.
        """
        # TODO: Edit this function to return the user id
        try:
            self.cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()

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
            # Check if user already exists
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                print("Username already existing on DB")
                return False
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Insert into DB
            self.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password.decode()))
            self.conn.commit()

            return True

        except Exception as e:
            print(f"Database error: {e}")
            return False

    # TODO: Implement other functions to interact with the DB