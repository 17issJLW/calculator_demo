class IllegalCharacter(Exception):

    def __init__(self, detail="非法字符"):
        self.detail = detail

class GrammarError(Exception):

    def __init__(self, detail="语法错误"):
        self.detail = detail