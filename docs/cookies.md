# Cookies

Arc has support for creating cookies. Cookies are data that the client browser stores for future use. Below is an example of how you can create cookies in an Arc application.

```py
from arc import App, TextResponse

app = App()

@app.route("/")
def setsession(request):
    response = TextResponse("Creating Cookies")
    response.set_cookie("data", "arc is AMAZING", max_age=app.to_seconds(10, "hour"))
    return response

@app.route("/getdata")
def getdata(request):
    return TextResponse(request.cookies.get("data"))

if __name__ == "__main__":
    app.run()
```

Lets break this down. Arc uses Starlettes Request and Response classes, which have support for getting and settings cookies. In our first route, we used the `.set_cookie()` method, and provided a key to access its data, the data, and the `max_age` parameter. The `max_age` paramter signifies how long the cookie will last in seconds. To make this easier for you, the `App` class has a `to_seconds()` method which takes an integer for the amount and a string which can either be `"hour"` or `"minute"`. In our second route, we use the `.cookies.get()` method to grab our stored cookie. Now, head to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see your app in action. Make sure not to go to the `/getdata` route before the `/` route, as it will raise an error.
