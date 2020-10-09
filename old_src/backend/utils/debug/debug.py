
import gc

class Debug:
    bug = None
    printable = 1
    @classmethod
    def dbg(cls, y): print(y)
    @classmethod
    def line_format(cls, line): return "Line %s --->>  "%line
    @classmethod
    def print_bug(cls, line, message, file=None):
        bug_line = cls.line_format(line)
        file = "File --> %s  "%file
        bug = file + bug_line + message
        cls.bug = bug
        if cls.printable: cls.dbg(bug)
    @classmethod
    def get_bug(cls): return cls.bug
    @classmethod
    def set_print(cls, val): cls.printable = val
    @classmethod
    def delete(cls, obj, up=False):
        if up: obj.delete(up)
        else: obj.delete()
    @classmethod
    def clear(cls): gc.enable(); gc.collect()
    @classmethod
    def printcol(cls, msg, col="blue"):
        black  = "\033[38;5;232m"
        if col == "yellow": color = "\033[48;5;30m"
        elif col == "blue": color = "\033[48;5;18m"
        elif col == "red": color = "\033[48;5;196m"
        elif col == "fred": color  = "\033[38;5;196m"
        elif col == "green": color  = "\033[48;5;30m"
        elif col == "white": color  = "\033[48;5;30m"
        back = "\033[0m"
