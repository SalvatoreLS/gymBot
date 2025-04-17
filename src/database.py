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

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def check_user(self, username : str, password : str) -> int|None:
        """
        Function to authorize a user and connect them to the right programs.
        Returns True if authentication is successful, otherwise False.
        """
        try:
            self.cursor.execute("SELECT id, password FROM gym_user WHERE username = ?", (username,))
            result = self.cursor.fetchone() # Returns a tuple (password_hash, id)

            if result is None:
                return None
            
            user_id = result[0]
            password_hash = result[1]

            if bcrypt.checkpw(password=password.encode(), hashed_password=password_hash.encode()):
                return user_id

            return None
        
        except Exception as e:
            print(f"Database error: {e}")
            return -1
    
    def check_username(self, username: str) -> bool:
        try:
            self.cursor.execute("SELECT id FROM gym_user WHERE username = ?", (username,))
            result = self.cursor.fetchone()

            return True if result is not None else False
        except Exception as e:
            print(f"Database error: {e}")
            return False
        
    def register_user(self, username : str, password : str) -> bool:
        """
        Function to register a new user and register data on the DB
        """
        try:
            # Check if user already exists
            self.cursor.execute("SELECT id FROM gym_user WHERE username = ?", (username,))
            existing_user = self.cursor.fetchone()

            if existing_user is not None:
                print("Username already existing on DB")
                return False
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Insert into DB
            self.cursor.execute("INSERT INTO gym_user (username, password_hash) VALUES (?, ?)", (username, hashed_password.decode()))
            self.conn.commit()

            return True

        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def get_programs(self, user_id):
        try:
            self.cursor.execute("SELECT id, name FROM program WHERE owner_id = ?", (user_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def get_programs_details(self, user_id) -> str:
        try:
            self.cursor.execute("SELECT id FROM program WHERE owner_id = ?", (user_id,))
            program_ids = self.cursor.fetchone()
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
        returned_string = ""

        try:
            for program_id in program_ids:
                self.cursor.execute("""
                                    SELECT program_day.day_number, program_day.name, exercise.name
                                    FROM program_day, exercise, program_day_exercise
                                    WHERE program_day.program_id = program.id AND exercise.id = program_day_exercise.exercise_id
                                        AND program_day_exercise.program_day_id = ?""", (program_id,))
                returned_string += self.program_details_to_string(self.cursor.fetchall())
        except Exception as e:
            print(f"Database error: {e}")
            return None
    

    def check_program(self, user_id, program_id):
        try:
            self.cursor.execute("""
                                SELECT id
                                FROM program
                                WHERE owner_id = ? AND id = ?)
                                """, (user_id, program_id))
            return self.cursor.fetchall() is not None
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def get_selected_program(self, user_id, program_id):
        # 1. Get all program_day_ids
        # 2. For each program_day_id get the last workout_id
        # 3. For the workout_id get all the sets performed
        try:
            self.cursor.execute("""
                                SELECT program_day.id
                                FROM program_day, program
                                WHERE program_id = ?
                                AND program.id = program_day.program_id
                                """, (program_id,))
            
            program_day_ids = self.cursor.fetchall()
        
        except Exception as e:
            print(f"Database error: {e}")
            return None

        try:
            for program_day_id in program_day_ids:
                # Get last workout id
                # CONTINUE FROM HERE
    # TODO: Implement other functions to interact with the DB


"""
SELECT
    pd.day_number,
    pd.name AS program_day_name,
    e.id AS exercise_id,
    e.name AS exercise_name,
    e.comment,
    e.extra_info,
    ws.weight,
    ws.reps,
    ws.rest,
    ws.sequence_number,
    w.workout_time,
    w.duration
FROM program p
JOIN program_day pd ON pd.program_id = p.id
JOIN program_day_exercise pde ON pde.program_day_id = pd.id
JOIN exercise e ON e.id = pde.exercise_id

-- Join performed workouts (optional, may be null if not yet performed)
LEFT JOIN workout_set ws ON ws.exercise_id = e.id
LEFT JOIN workout w ON w.id = ws.workout_id AND w.user_id = p.owner_id

WHERE p.id = 1 AND p.owner_id = 1
ORDER BY pd.day_number, e.id, ws.sequence_number;

day_number | program_day_name | exercise_id | exercise_name |         comment          |          extra_info           | weight | reps | rest | sequence_number |        workout_time        | duration 
------------+------------------+-------------+---------------+--------------------------+-------------------------------+--------+------+------+-----------------+----------------------------+----------
          1 | Push Day         |           1 | Bench Press   | Barbell chest press      | Recommended warm-up included  |     50 |   10 |   90 |               1 | 2025-04-15 14:28:28.472151 |       60
          1 | Push Day         |           1 | Bench Press   | Barbell chest press      | Recommended warm-up included  |     55 |    8 |   90 |               2 | 2025-04-17 14:28:28.472151 |       70
          1 | Push Day         |           2 | Squat         | Barbell back squat       | Use rack for safety           |     80 |    8 |  120 |               2 | 2025-04-15 14:28:28.472151 |       60
          2 | Pull Day         |           3 | Deadlift      | Classic compound lift    | Maintain form to avoid injury |    100 |    5 |  180 |               1 |                            |         
          2 | Pull Day         |           4 | Pull-up       | Bodyweight back exercise | Add weight if too easy        |      0 |   12 |   60 |               1 | 2025-04-17 14:28:28.472151 |       70
"""