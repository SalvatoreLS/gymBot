import pandas as pd
import re

class ExerciseSet:
    """
    Class for each set of an exercise
    """
    def __init__(self):
        self.weight = None
        self.rest = None
        self.reps = None
    
    def fill_set(self, weight: float, rest: int, reps: int):
        self.weight = weight
        self.rest = rest
        self.reps = reps

    def update_weight(self, new_weight: float):
        self.weight = new_weight

    def update_rest(self, new_rest: int):
        self.rest = new_rest
    
    def update_reps(self, new_reps: int):
        self.reps = new_reps

    def to_string(self):
        return f"{'Reps:':<6} {self.reps:<3} | {'Weight:':<7} {self.weight:<5}kg | {'Rest:':<5} {self.rest:<3}s"


class Exercise:
    """
    Class for each single exercise
    """
    def __init__(self):
        self.id = None
        self.name = None
        self.comment = None
        self.extra_info = None
        self.updated = None
        self.sets = []

    def set_name(self, name: str):
        self.name = name
    
    def set_id(self, id: int):
        self.id = id
    
    def set_comment(self, comment: str):
        self.comment = comment
    
    def set_extra_info(self, extra_info: str):
        self.extra_info = extra_info
    
    def set_exercise_sets(self, new_sets: str[ExerciseSet]):
        self.sets = new_sets

    def add_set(self, new_set: ExerciseSet):
        self.sets.append(new_set)

    def to_string(self):
        string_exercise = f"\n{self.name}:\n"
        for i, s in enumerate(self.sets):
            string_exercise += f"  Set {i+1}: {s.to_string()}\n"
        return string_exercise

    def get_last_set(self):
        return self.sets[-1]

class DayProgram:
    """
    Class for each day of a program
    """
    def __init__(self):
        self.id = None
        self.day_number = None
        self.day_name = None
        self.exercises = []

    def set_id(self, id: int):
        self.id = id

    def set_day_number(self, day_number: int):
        self.day_number = day_number

    def set_day_name(self, day_name: str):
        self.day_name = day_name

    def add_exercise(self, new_exercise: Exercise):
        self.exercises.append(new_exercise)

    def to_string(self) -> str:
        return_string = f"\n=== Day {self.day_number}: {self.day_name} ===\n"
        for exercise in self.exercises:
            return_string += exercise.to_string()
        return return_string


class Program:
    """
    Class for each program
    """
    def __init__(self):
        self.id = None
        self.program_name = None
        self.days = []

    def set_id(self, id: int):
        self.id = id
    
    def set_program_name(self, program_name: str):
        self.program_name = program_name
    
    def add_day(self, new_day: DayProgram):
        self.days.append(new_day)
    
    def to_string(self) -> str:
        return_string = f"🏋️ Program: {self.program_name} 🏋️\n"
        for day in self.days:
            return_string += day.to_string()
        return return_string 