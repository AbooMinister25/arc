# from app import App


class DefaultExceptionHandler:
    def __init__(self):
        # self.app = App(f"arc/templates")
        ...
    
    def handle_error(self, request, response, error):
        response.text = "ERROR"