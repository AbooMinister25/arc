"""
The below is COMING SOON
"""



# from arc.middleware import Middleware
# import secrets


# class SessionHandler:
#     def __init__(self, app):
#         self.app = app
#         self.lifetime = self.app.to_seconds(1, "hour")

#         self._dict = {}

#     def init_session(self, response):
#         key = secrets.token_urlsafe(20)
#         response.set_cookie("secret_key", key,
#                             httponly=True, max_age=self.lifetime)
#         return response


# class SessionMiddleware(Middleware):
#     def process_request(req):
#         ...

#     def process_response(req, res):
#         key = secrets.token_urlsafe(20)
#         res.set_cookie("secret_key", key)
