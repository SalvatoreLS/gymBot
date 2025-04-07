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
        self.comment = None
        self.extra_info = None
    
    def fill_set(self, weight: float, rest: int, reps: int, extra_info: str = None, comment: str = None):
        self.weight = weight
        self.rest = rest
        self.reps = reps
        self.extra_info = extra_info
        self.comment = comment

    def update_weight(self, new_weight: float):
        self.weight = new_weight

    def update_rest(self, new_rest: int):
        self.rest = new_rest
    
    def update_reps(self, new_reps: int):
        self.reps = new_reps
    
    def update_extra_info(self, new_info: str):
        self.extra_info = new_info
    
    def update_comment(self, comment: str):
        self.comment = comment

    # TODO: Add functions to get set as formatted string

class Exercise:
    """
    Class for each single exercise
    """
    def __init__(self):
        self.sets = []
    
    # TODO: Add functions to get exercise as formatted string

class DayProgram:
    """
    Class for each day of a program
    """
    def __init__(self):
        self.day_name = None
        self.exercises = []
    
    # TODO: Implement all the other functions and variables

class Program:
    """
    Class for each program
    """
    def __init__(self):
        self.program_name = None
        self.days = []

    # TODO: Implement all the functions
