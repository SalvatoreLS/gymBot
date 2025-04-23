from utils import resolve_class
class StateGraph:
    def __init__(self):

        self.state_class_registry = {
            "authenticated": "telegram_bot.state_handlers.authenticated_state.AuthenticatedStateHandler",
            "dead": "telegram_bot.state_handlers.dead_state.DeadStateHandler",
            "end": "telegram_bot.state_handlers.end_state.EndStateHandler",
            "login": "telegram_bot.state_handlers.login_state.LoginStateHandler",
            "ready": "telegram_bot.state_handlers.ready_state.ReadyStateHandler",
            "started": "telegram_bot.state_handlers.started_state.StartedStateHandler",
            "type_day": "telegram_bot.state_handlers.type_day_state.TypeDayStateHandler",
            "type_program": "telegram_bot.state_handlers.type_program_state.TypeProgramStateHandler"
        }

        self.state_successions = {
            "dead": "login",
            "login": "authenticated",
            "authenticated": "type_program",
            "type_program": "type_day",
            "type_day": "ready",
            "ready": "started",
            "started": "end",
            "end": "authenticated"
        }

    def get_next_state(self, current_state: str):
        """
        Returns the next state based on the current state.
        """
        next_state_key = self.state_successions.get(current_state)
        class_path = self.state_class_registry[next_state_key]
        return resolve_class(class_path)