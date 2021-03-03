# Sessions

Arc has support for creating web sessions. If you don't know what they are, sessions are basically temporary pieces of data that the server stores for future reference. Sessions are often confused with cookies, but cookies are stored on the client end, and sessions are stored on the server, making them more secure. Arc has a very straightforward way to implement sessions into your application. Just copy and paste the following code into your python file.

```py
from arc import App, TextResponse, SessionHandler

app = App()

session = SessionHandler(app)

@app.route("/")
async def index(request):
    response = TextResponse("Sessions are cool :D")
    session.init_session(request, response)
    session()["data"] = "Arc is AMAZING"
    return response


@app.route("/getsession")
async def getsession(request):
    return TextResponse(f"Session Data: {session()["data"]}")

if __name__ == "__main__":
    app.run()
```

Alright, so you may have noticed that we have imported a new class, the `SessionHandler` class, which is used to create and use sessions. We called it using the `init_session` method, and interact with it similarly to a dict like object. By default, sessions last one hour, and expire after that, you do the following.

```py
session = SessionHandler(app, lifetime=app.to_seconds(48, "hour"))
```
You can also optionally pass a secret key, like the following.

```py
import secrets
...
session = SessionHandler(app, secret_key=secrets.tokens.urlsafe(20))
```
Your secret key is added to the unique session token that is generated each time a new session is opened. At the moment, sesions are still being developed, so feel free to open an issue on any problems or risks with the security of the sessions, or make a pull request.