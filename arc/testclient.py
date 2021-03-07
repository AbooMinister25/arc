"""
COMING SOON
"""


# import requests


# class TestClient:
#     def __init__(self, app, url: str = None):
#         self.app = app
#         self.host = app.host
#         self.port = app.port

#         if url is not None:
#             self.url = url
#         else:
#             self.url = f"http://{self.host}:{self.port}"

#     def full_test_app(self):
#         responses = []

#         for path, items in self.app.routes.items():
#             try:
#                 methods = items["methods"]
#             except:
#                 methods = ["GET", "POST", "HEAD", "PUT", "DELETE",
#                            "CONNECT", "OPTIONS", "TRACE", "PATCH"]

#             if "get" in [method.lower() for method in methods]:
#                 response = requests.get(f"{self.url}{path}")

#                 assert response.status_code == 200

#                 responses.append(response)
#                 continue

#             for method in methods:
#                 if method.lower() != "connect" and method.lower() != "trace":
#                     pass
#                 else:
#                     response = getattr(requests, method.lower())(
#                         f"{self.url}{path}")
