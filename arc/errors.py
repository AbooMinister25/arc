class AppException:
    def __init__(self, app, error_pages={"404": "default", "500": "default"}):
        self.app = app
        self.error_pages = error_pages