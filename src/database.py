import psycopg2
import pandas as pd
import bcrypt

from typing import List, Tuple

from program_classes import ExerciseSet, Exercise, DayProgram, Program

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
            self.cursor.execute("SELECT id, password FROM gym_user WHERE username = %s;", (username,))
            result = self.cursor.fetchone() # Returns a tuple (id, password_hash)

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
            self.cursor.execute("SELECT id FROM gym_user WHERE username = %s", (username,))
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
            self.cursor.execute("SELECT id FROM gym_user WHERE username = %s", (username,))
            existing_user = self.cursor.fetchone()

            if existing_user is not None:
                print("Username already existing on DB")
                return False
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Insert into DB
            self.cursor.execute("INSERT INTO gym_user (username, password_hash) VALUES (%s, %s)", (username, hashed_password.decode()))
            self.conn.commit()

            return True

        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def get_programs(self, user_id):
        try:
            self.cursor.execute("SELECT id, name FROM program WHERE owner_id = %s", (user_id,))
            return self.programs_to_string(self.cursor.fetchall())
        except Exception as e:
            print(f"Database error: {e}")
            return None
        
    def programs_to_string(self, programs) -> str:
        returned_string = ""
        for row in programs:
            returned_string += f"{row[0]}) {row[1]}\n"
        return returned_string

    def get_programs_details(self, user_id) -> str:
        try:
            self.cursor.execute("SELECT id FROM program WHERE owner_id = %s", (user_id,))
            program_ids = self.cursor.fetchone()
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
        returned_string = ""

        try:
            for program_id in program_ids:
                self.cursor.execute("""
                                    SELECT pd.day_number, pd.name, e.name
                                    FROM program_day pd, exercise e, program_day_exercise pde, program p
                                    WHERE pd.program_id = p.id AND e.id = pde.exercise_id
                                        AND pde.program_day_id = %s
                                        AND p.owner_id = %s
                                    ORDER BY pd.day_number""", (program_id, user_id))
                returned_string += self.program_details_to_string(self.cursor.fetchall())
                return returned_string
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def program_details_to_string(self, program_details) -> str:
        returned_string = ""
        day_number = 0
        for row in program_details:
            if day_number != row[0]:
                returned_string += f"\n{row[0]}) {row[1]}\n"
                day_number = row[0]
            returned_string += f"\t- {row[2]}\n"
        return returned_string[:-1]
    
    def check_program(self, user_id, program_id):
        try:
            self.cursor.execute("""
                                SELECT id
                                FROM program
                                WHERE owner_id = %s AND id = %s
                                """, (user_id, int(program_id)))
            return self.cursor.fetchall() is not None
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def get_selected_program(self, user_id: int, program_id: int) -> Program|None:
        """
        1. Get all program_day_ids
        2. For each program_day_id get the last workout_id
        3. For the workout_id get all the sets performed
        """
        new_program = Program()

        new_program_days = []

        try:
            # Get program name
            self.cursor.execute("""
                                SELECT p.name, p.id
                                FROM program p
                                WHERE p.id = %s AND p.owner_id = %s
                                """, (program_id, user_id))
            result = self.cursor.fetchone()
        except Exception as e:
            print(f"Database error while getting program name: {e}")
            return None

        # Set program name and id
        new_program.set_id(id=program_id)
        new_program.set_program_name(program_name=result[0])

        try:
            # Get program day ids
            self.cursor.execute("""
                                SELECT program_day.id
                                FROM program_day, program
                                WHERE program_id = %s
                                AND program.id = program_day.program_id
                                ORDER BY program_day.day_number;
                                """, (program_id,))
            result = self.cursor.fetchall()
        except Exception as e:
            print(f"Database error while getting program day ids: {e}")
            return None

        program_day_ids = result

        try:
            for program_day_id in program_day_ids:
                # Get last workout id
                self.cursor.execute("""
                                    SELECT w.id
                                    FROM workout w, workout_set ws, program_day_exercise pde
                                    WHERE w.id = ws.workout_id AND ws.exercise_id = pde.exercise_id
                                        AND user_id = %s AND program_day_id = %s
                                    ORDER BY workout_time DESC
                                    LIMIT 1;
                                    """, (user_id, program_day_id[0]))
                workout_id = self.cursor.fetchone()

                self.cursor.fetchall()

                # Get all info about exercises in last workout
                self.cursor.execute("""
                                    SELECT e.id, e.name, e.comment, e.extra_info,
                                        ws.weight, ws.reps, ws.rest, ws.sequence_number
                                    FROM exercise e, workout_set ws
                                    WHERE e.id = ws.exercise_id
                                        AND ws.workout_id = %s
                                    ORDER BY ws.sequence_number ASC;
                                    """, (workout_id[0],))
                
                # Parse results and collect formatted exercises
                exercises = self.__parse_exercises(exercises=self.cursor.fetchall())
                
                # Get Program Day details and fill the program
                self.cursor.execute("""
                                    SELECT pd.day_number, pd.name
                                    FROM program_day pd
                                    WHERE pd.program_id = %s AND pd.id = %s
                                    ORDER BY day_number ASC;
                                    """, (program_id, program_day_id[0]))
                
                result = self.cursor.fetchone()

                new_program_days.append(DayProgram())
                new_program_days[-1].set_id(id=program_day_id[0])
                new_program_days[-1].set_day_number(day_number=result[0])
                new_program_days[-1].set_day_name(day_name=result[1])
                new_program_days[-1].set_exercises(new_exercises=exercises)
            
            new_program.set_days(new_days=new_program_days)
            return new_program
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def __parse_exercises(self, exercises: List[Tuple]) -> List[Exercise]:
        """
        Takes the result of exercises query execution and fills an exercise structure.
        It expects (id, name, comment, extra_info, weight, reps, rest, sequence_number)
        """
        prev_id = -1
        exercises_list = []

        for row in exercises:
            if prev_id == row[0]:
                # TODO: Sets are always empty
                exercises_list[-1].add_set(
                    ExerciseSet().fill_set(
                        weight=float(row[4]),
                        rest=row[6],
                        reps=row[5]
                    )
                )
            else:
                exercises_list.append(
                    self.__fill_exercise(row=row, exercise=Exercise()))
                new_set = ExerciseSet()
                new_set.fill_set(
                    weight=float(row[4]),
                    rest=row[6],
                    reps=row[5]
                )
                exercises_list[-1].add_set(new_set)
            prev_id = row[0]

        return exercises_list

    def __fill_exercise(self, row, exercise):
        exercise.set_id(row[0])
        exercise.set_name(row[1])
        exercise.set_comment(row[2])
        exercise.set_extra_info(row[3])
        return exercise
    
    def update_set(self, user_id: int, program_id: int, day_id: int, exercise_id: int, set_numer: int, what_to_update: str, new_value: int) -> bool:
        """
        Function to update a set in the database
        """
        try:
            self.cursor.execute("""
                                UPDATE workout_set ws
                                SET weight = %s, reps = %s, rest = %s
                                FROM workout w, program_day_exercise pde
                                WHERE ws.workout_id = w.id AND pde.exercise_id = ws.exercise_id
                                    AND w.user_id = %s AND w.program_day_id = %s
                                    AND pde.program_day_id = %s AND pde.exercise_id = %s
                                    AND ws.sequence_number = %s;
                                """, (new_value if what_to_update == "weight" else None,
                                      new_value if what_to_update == "reps" else None,
                                      new_value if what_to_update == "rest" else None,
                                      user_id, program_id, day_id, exercise_id, set_numer))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Database error while updating set: {e}")
            return False