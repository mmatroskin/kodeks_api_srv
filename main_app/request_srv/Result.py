class Result:

    def __init__(self, url=None, status=None):
        self.status = status
        self.data = None
        self.url = url
        self.message = 'Error'
        self.headers = {}
