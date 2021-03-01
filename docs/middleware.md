# Middleware


Arc has support for adding custom middlewares. If you don't know what it is, middleware is basically a component that you can use to modify the behavior of an incoming request or an outgoing response. By default, Arc has a middleware created that logs requests and responses onto the console. You may have noticed this, as each time you make a request, it's logged in the console, alongside the outgoing response. In order to make custom middlewares, you have to use Arc's `Middleware` class. Copy the following code into your python file.

```py
from arc import App, Middleware, TextResponse

app = App()

class CustomMiddleware(Middleware):
    def process_request(self, req):
        print("Recieved a request")
    
    def process_response(self, req, res):
        print("Sent a response")

app.add_middleware(CustomMiddleware)

@app.route("/")
def index(request):
    return TextResponse("Middlewares are cool :D")

if __name__ == "__main__":
    app.run()
```

Lets break this down. As you may have noticed, we imported the `Middleware` class to help us construct our custom middleware. Then we created the `CustomMiddleware`
class which consists of the `process_request()` and `process_response()` methods. These methods decide what to do in order to handle a response or request, in our case, they are printing to the console each time a request is made or a response is given. Now lets run our code. Head to [http://127.0.0.1:5000](http://127.0.0.1:5000), and back to your code. Something like below should have appeared.

```
INFO: Running on http://127.0.0.1:5000

INFO: Press CTRL + C to stop
Recieved a request

INFO: [REQUEST][GET] http://127.0.0.1:5000/

INFO: [RESPONSE] http://127.0.0.1:5000/
Sent a response
Recieved a request

INFO: [REQUEST][GET] http://127.0.0.1:5000/favicon.ico

INFO: [RESPONSE] http://127.0.0.1:5000/favicon.ico
Sent a response
```

Congratulations, your custom middleware worked. Now, above, we have two middlewares at work here, the default one, and our custom one. In some cases, we may not want the default middleware clogging up the console if we have our own custom one running, because of this, you can disable the default middleware. In order to do this, edit your current code so it looks like the following.

```py
from arc import App, Middleware

app = App(logging=False)

class CustomMiddleware(Middleware):
    def process_request(self, req):
        print("Recieved a request")
    
    def process_response(self, req, res):
        print("Sent a response")

app.add_middleware(CustomMiddleware)

@app.route("/")
def index(req, res):
    res.text = "Middlewares are cool :D"

if __name__ == "__main__":
    app.run()
```

Now run your app and head to [http://127.0.0.1:5000](http://127.0.0.1:5000) once again. If you look back at the console again, you should see something like this.

```
[INFO] Running on http://127.0.0.1:5000
[INFO] Press CTRL + C to stop

Recieved a request
Sent a response
```

As you may have noticed, the default middleware has disappeared, and theres only our middleware left.