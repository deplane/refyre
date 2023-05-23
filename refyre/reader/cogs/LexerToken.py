import fnmatch

class Token:
    '''
        A single Lexer token
    '''
    def __init__(self, tab_level, pattern = "", dir = "",  type = "", name = "", flags = "", serialize=""):
        self.tab_level = tab_level
        self.pattern = pattern
        self.directory = dir
        self.dirtype = type
        self.name = name
        self.flags = flags
        self.serialize = serialize

    def __repr__(self):
        return f"Token(tab_level={self.tab_level},pattern={self.pattern},directory={self.directory},dirtype={self.dirtype},name={self.name},flags={self.flags},serialize={self.serialize})"
