class MockResponse:

    def __init__(self, status_code: int, text: str = ''):
        self.status_code = status_code
        self.text = text
