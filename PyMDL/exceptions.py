# code- 1: invalid url, 2: doesn't belong to MDL.

class InvalidURLError(Exception):
    def __init__(self, value: str):
        self.value = value
        self.code = 1
        self.message = f"Entered string is not a valid URL!\nURL:{self.value}\nError Code:{self.code}"
        super().__init__(self.message)


class NotMDLError(Exception):
    def __init__(self, value):
        self.value = value
        self.code = 2
        self.message = f"Entered string does not belong to MDL!\nURL:{self.value}\nError Code:{self.code}"
        super().__init__(self.message)


class BadHttpResponseError(Exception):
    def __init__(self, value, code):
        self.value = value
        self.code = code
        if self.code == 404:
            self.message = f'The page could not be found!\nURL:{self.value}\nError Code:{self.code}'
        else:
            self.message = f"Entered string belongs to MDL but is resulting in a bad request!\nURL:{self.value}\nError Code:{self.code}"
        super().__init__(self.message)


class RequestTimeoutError(Exception):
    def __init__(self):
        self.code = -1
        self.message = f"Cannot send request! Check your internet connection!\nError Code:{self.code}"
        super().__init__(self.message)
