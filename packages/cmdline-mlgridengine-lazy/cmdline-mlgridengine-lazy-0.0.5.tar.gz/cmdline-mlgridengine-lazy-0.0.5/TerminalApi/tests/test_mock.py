class MockResponse:
    def __init__(self, content, status_code, headers=None, raw=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.raw = raw

    def json(self):
        return self.content
