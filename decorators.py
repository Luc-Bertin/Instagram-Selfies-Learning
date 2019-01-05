class NbCallFunction:
    def __init__(self, function):
        self.callNumber = 0
        self.function = function
    def __call__(self, *args, **kwargs):
        #onCall
        self.callNumber += 1
        return self.function(*args, **kwargs)