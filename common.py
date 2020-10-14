class ScriptException(Exception):
    """Custom exception class with message for this module."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)
