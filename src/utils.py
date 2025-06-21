import importlib

def resolve_class(class_path: str):
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

def get_reply_markup(next_state):

    # keys = next_state.__class__.get_callbacks()
    keys = next_state.callbacks

    if len(keys) % 2 != 0:
        keys.append("- - -")
    
    markup_keyboard = []

    for i in range(0, len(keys), 2):
        markup_keyboard.append(keys[i:i+2])
    return markup_keyboard