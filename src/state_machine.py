from enum import Enum

class State(Enum):
    DEAD = 0
    LOGIN = 1
    AUTHENTICATED = 2
    TYPE_PROGRAM = 3
    TYPE_DAY = 4
    READY = 5
    STARTED = 6
    END = 7

class SubStateUpdateSet(Enum):
    NONE = 0
    TYPE_SET = 1 # User types which set to update (1, 2, 3, 4, ..., current)
    TYPE_WHAT = 2 # User types what to update (reps, weight, etc.)
    TYPE_NEW_VALUE = 3 # User types the new value for the exercise

class SubStateLogin(Enum):
    NONE = 0
    USERNAME = 1
    PASSWORD = 2
    AUTHENTICATED = 3

class SubStateUpdateExercise(Enum):
    NONE = 0
    TYPE_EXPRESSION = 1 # User types the expression for updating the exercise

class StateMachine:
    def __init__(self):
        self.state = State.DEAD
        self.substate_update_set = SubStateUpdateSet.NONE
        self.substate_update_exercise = SubStateUpdateExercise.NONE
        self.substate_login = SubStateLogin.NONE

    # Setters and Getters

    # Main state
    def set_state(self, state: State):
        self.state = state

    def get_state(self) -> State:
        return self.state

    # Substate update set
    def set_substate_update_set(self, substate: SubStateUpdateSet):
        self.substate_update_set = substate
    
    def get_substate_update_set(self) -> SubStateUpdateSet:
        return self.substate_update_set
    
    # Substate update exercise
    def set_substate_update_exercise(self, substate: SubStateUpdateExercise):
        self.substate_update_exercise = substate
    
    def get_substate_update_exercise(self) -> SubStateUpdateExercise:
        return self.substate_update_exercise
    
    # Substate login
    def set_substate_login(self, substate: SubStateLogin):
        self.substate_login = substate
    
    def get_substate_login(self) -> SubStateUpdateSet:
        return self.substate_login
