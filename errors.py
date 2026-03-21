sty = {
    "reset": "\x1b[0m",
    "red": "\x1b[91m",
    "dim": "\x1b[2m"}

class ExceptionHandler:
    def __init__(self):
        self.messages = {
            FileNotFoundError: "Solus couldn't locate that file.",
            FileExistsError: "That file already exists.",
            IsADirectoryError: "That is a directory.",
            NotADirectoryError: "That is not a directory.",
            MemoryError: "Not enough working memory to perform this task.",
            UnicodeError: "Contains Unicode bytes that cannot be converted to ASCII.",
            OverflowError: "Result is too large to be represented.",
            ImportError: "Failed to import necessary module(s).",
            KeyError: "Solus failed to identify that key.",
            TypeError: "Incorrect data type.",
            ValueError: "The value provided is invalid.",
            IndexError: "Invalid number of arguments.",
            PermissionError: "Solus doesn't have permission to perform this task.",
            RecursionError: "Performed the same operation 1,000 times."}
        self.warnings = {
            UnicodeWarning: "Unicode conversion to ASCII attempted.",
            ResourceWarning: "System resources nearing limits.",
            DeprecationWarning: "Uses functions that are deprecated."}

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return self.format_error(e)
            except Warning as w:
                return self.format_warning(w)
        return wrapper

    def format_error(self, error):
        custom = self.messages.get(type(error), "Something went wrong.")
        return f"{sty['red']}[{type(error).__name__}]{sty['reset']} {custom} {sty['dim']}({str(error)}){sty['reset']}"
    def format_warning(self, warning):
        custom = self.warnings.get(type(warning), "Something went wrong.")
        return f"{sty['red']}[{type(warning).__name__}]{sty['reset']} {custom} {sty['dim']}({str(warning)}){sty['reset']}"