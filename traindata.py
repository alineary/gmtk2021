class FirstClass:
    def __init__(self):
        super().__init__()
        self.blacklist = []
        self.needlist = []


class SecondClass:
    def __init__(self):
        super().__init__()
        self.blacklist = []
        self.needlist = [FirstClass]

