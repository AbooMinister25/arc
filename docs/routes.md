# Routes

If you've used a web framework before, you know that you have to define routes in your application. Routes are sort of like highways that send requests to the code that handles them. In Arc, there are two ways you can create routes, one of which uses decorators, similar to Flask and Bottle, and the other takes inspiration from Django. Below is how you can create routes using Arcs default decorator syntax.

```py
from arc import App, TextResponse

app = App()

@app.route("/home")
def home(request):
    return TextResponse("Welcome to the home page")

@app.route("/")
def index(request):
    return TextResponse("Go to http://localhost:5000/home to see the home page")

if __name__ == "__main__":
    app.run()
```
The above code is signifying two different routes. One of which is `/home`, which executes the code in the `home()` function defined here. Another specifies the `/` route, which points to http://localhost:5000. If you prefer a more Django like routing style, you can do the below.

```py
from arc import App, TextResponse

app = App()

def home(request):
    return TextResponse("Welcome to the home page")

def index(request):
    return TextResponse("Go to http://localhost:5000/home to see the home page")

app.add_route("/home", home)
app.add_route("/", index)

if __name__ == "__main__":
    app.run()
```
The above does the exact same thing as the first example with decorators, but instead of a decorator based routing system, we're using the `App` class's `.add_route` method. Now lets take a closer look at the handlers. A basic handler is structured as the following.
```py
def handler_name(request):
    # handler code
```

When making routes, you can also specify what request methods are allowed for the route, such as the following.

```py
from arc import App, TextResponse

app = App()

@app.route("/", methods=["GET"])
def home(request):
    return TextResponse("Only get requests are allowed on this route")

if __name__ == "__main__":
    app.run()
```

In the above, if you try something other than a GET request, you'll get an error.

You have a function name, which you can define as anything you want, one parameter, which represent the `request`, and the contents of the handler, which decide what to do. You can use different response types to add content to the web page. You can also use query parameters in your routes. Query parameters are similar to path parameters, but are optional, and you don't set them as a variable in your handler. They can be used as the below.

```py
from arc import App, TextResponse

app = App()

@app.route("/")
def index(request):
    return TextResponse(request.query_params["data"])

if __name__ == "__main__":
    app.run()
```

Now, in the above, we're using the `request` variable to access our query parameters. Run your app, and head to [http://127.0.0.1:5000/?data=test](http://127.0.0.1:5000/?data=test) and you should see the words `test` on your screen. In our route, we're specifiying query parameters by doing `/?key=value`, where the key is what our query parameter is called inside our `query_params` dict. If you run the above without specifying `data`, your application will raise an error, so if you use query params, make sure to have something in place that'll allow you to check whether the query parameter you want is entered.