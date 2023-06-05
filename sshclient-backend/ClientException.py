class NoConnectionException(Exception):
    def __init__(self, error: str):
        super().__init__(self)
        self.error = error

    def __str__(self):
        return repr(self.error)


class InitException(Exception):
    def __init__(self, error:str):
        super().__init__(self)
        self.error = error

    def __str__(self):
        return repr(self.error)