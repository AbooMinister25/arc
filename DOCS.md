# Arc Documentation

### Arc is a python ASGI web framework for creating fast and dynamic web applications.

# Contents
- [Arc Documentation](#arc-documentation)
    - [Arc is a python ASGI web framework for creating fast and dynamic web applications.](#arc-is-a-python-asgi-web-framework-for-creating-fast-and-dynamic-web-applications)
- [Contents](#contents)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Routes](#routes)
- [Templates](#templates)
  - [Serving static files](#serving-static-files)
- [Cookies](#cookies)
- [Middleware](#middleware)
- [Collections](#collections)
- [Responses](#responses)
- [Async](#async)
- [Deployment](#deployment)
- [Afterword](#afterword)



# Installation
Arc is relatively easy to get set up, and can be installed using `pip`.
```
# Windows

pip install arcframework

# Linux

pip3 install arcframework
```


# Quickstart
Arc is very straightforward and simple to use, and its structured similarly to other micro frameworks such as Flask or Bottle. Once you've installed Arc, copy and paste the below code into your editor.
```py
from arc import App, TextResponse

app = App()

@app.route("/")
def home(request):
    return TextResponse("Hello, World")

if __name__ == "__main__": 
    app.run()
```
Alright, lets break this code down. Arc has a single `App` module that you need to import in order to create your web app. The `App` module has all of the methods that you'll need in order to create a basic web application. Once you initialize the `App` module, you can then use a decorator to define a route. You can than define a function to be the handler that is called when that route is invoked. Lastly, we check if the file is being run directly, and run our web application. Now, run the code you just copy and pasted, once you've done that, you should see something like the below in your console.
```
[INFO] Running on http://127.0.0.1:5000
[INFO] Press CTRL + C to stop
```
Great, you've successfully run your web application! Head over to http://127.0.0.1:5000 to see your web application in action. Once you're there, you should see the text `Hello World` displayed on the screen.

# Routes
If you've used a web framework before, you know that you have to define routes in your application. Routes are sort of like highways that send requests to the code that handles them. In Arc, there are two ways you can create routes, one of which uses decorators, similar to Flask and Bottle, and the other takes inspiration from Django. Below is how you can create routes using decorators.
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
The above code is signifying two different routes. One of which is `/home`, which executes the code in the `home()` function defined here. Another specifies the `/` route, which is just http://localhost:5000. If you prefer a more Django like routing style, you can do the below.
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
You have a function name, which you can define as anything you want, one parameter, which represent the `request`, and the contents of the handler, which decide what to do. You can use different response types to add content to the web page.
# Templates
Like any other web framework, Arc has support for HTML templates, and uses jinja2 for templating. If you've ever used Flask, this should be very familiar, as Flask uses jinja2's templating syntax as well. Arc has a very straightforward way for creating templates. First, create a `templates` directory in your current working folder. Jinja2 will search for templates in a `templates` directory, though you are able to change that. Inside the `templates` directory you just created, make an `index.html` file, and copy and paste the following content into it.
```html
<!DOCTYPE html>
<html>
    <head>
        <title>{{title}}</title>
    </head>
    <body>
        <h1>{{heading}}</h1>
    </body>
</html>
```
Once you've done that, save and close the file, and go back to the python file you were working in. Add the following code to the file.
```py
from arc import App, Template

app = App()

template = Template()

@app.route("/")
def index(request):
    return template("index.html", context={"request": request, "title": "Templates", "heading": "Arc is AMAZING"})

if __name__ == "__main__":
    app.run()
```
Once you have that, run your file and head to http://127.0.0.1:5000 to see your web page in action. Once you're there, you should see the text `Arc is AMAZING` on the screen. Now, lets break down what we've done here. Instead of importing `TextResponse` like before, we used Arc's `Template` class. The `Template` class behaves just like a response, and requires you to fill out a template name, and the context, which is a dict. You are required to provide `request` to the context as a key. By default, the `Template` class searches for templates in the `templates` directory, but you can change that by doing the following.
```py
from arc import App, Template

app = App()
template = Template(directory="pages")
```
If you do the above, arc will then search for templates in the `pages` directory.
## Serving static files
Whats a good web page without decent styling? Luckily for us, `Arc` has support for serving static files. First, lets create a directory called `static` in our current working folder. Inside the new `static` folder, create a `style.css` file and put the following code in it.
```css
body {
    background-color: orange;
}
```
Now, go to the `index.html` file and change it so it looks like the following.
```html
<!DOCTYPE html>
<html>
    <head>
        <title>{{title}}</title>
        <link rel="stylesheet" href="static/style.css">
    </head>
    <body>
        <h1>{{heading}}</h1>
    </body>
</html>
```
You don't have to make any changes to your app, just restart your web application and head back to http://127.0.0.1:5000. Once you're there, the background of the page should now be orange. Similarly to how you can change the default templates folder, you can also change the default `static` folder to something else like below.
```py
from arc import App

app = App(static_dir="styles")
```
Now, the code will serve static files from the `styles` directory.

# Cookies
Arc has support for creating cookies. Cookies are data that the client browser stores for future use. Below is an example of how you can create cookies.
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
Lets break this down.  Lets break this down. Arc uses Starlettes Request and Response classes, which have support for getting and settings cookies. In our first route, we used the `.set_cookie()` method, and provided a key to access its data, the data, and the `max_age` parameter. The `max_age` paramter signifies how long the cookie will last in seconds. To make this easier for you, the `App` class has a `to_seconds()` method which takes an integer for the amount and a string which can either be `"hour"` or `"minute"`. In our second route, we use the `.cookies.get()` method to grab our stored cookie. Now, head to http://127.0.0.1:5000 to see your app in action. Make sure not to go to the `/getdata` route before the `/` route, as it will raise an error.

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
class which consists of the `process_request()` and `process_response()` methods. These methods decide what to do in order to handle a response or request, in our case, they are printing to the console each time a request is made or a response is given. Now lets run our code. Head to http://127.0.0.1:5000, and back to your code. Something like below should have appeared.
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
Now run your app and head to http://127.0.0.1:5000 once again. If you look back at the console again, you should see something like this.
```
[INFO] Running on http://127.0.0.1:5000
[INFO] Press CTRL + C to stop

Recieved a request
Sent a response
```
As you may have noticed, the default middleware has disappeared, and theres only our middleware left.

# Collections
Everything that we've been doing so far has been inside a single python file. For us, this is completely fine, but say you were working on a larger application, a single python file would get confusing to navigate and use. For that very reason, Arc has a class called `Collection`. This class does sort of the same thing as Flask's `Blueprint` class. The `Collection` class basically groups together a set of routes which can then be appended to the main `App` object, allowing your code to be spread out across multiple python files. Alright, open a new project directory, and make two python files, `__init__.py` and `test.py`. Copy and paste the following code into `__init__.py`.
```py
from arc import App
from .test import mycollection

app = App()
app.register_collection(mycollection)

if __name__ == "__main__":
    app.run()
```
The above code is initializing our app, as normal, but its importing a `mycollection` object from `test.py`, which we'll make in a moment, and using the `App` class's `.register_collection` function to add the `mycollection` module to our main app. Now, for `test.py`, copy and paste the following code into it.
```py
from arc import Collection, TextResponse

mycollection = Collection()

@mycollection.route("/")
def index(request):
    return TextResponse("Collections are cool :D")
```
As you can see above, a collection behaves almost exactly like the main app class, and has most of the same methods, and the ability to serve HTML templates and create cookies, so you're not losing anything by using a collection. Alright, lets test this out, run your `__init__.py` file and head to http://127.0.0.1:5000 to see your app in action.

# Responses
As you may have noticed throughout this documentation, we have been using the `TextResponse` class, which renders text on our web page. Arc has support for many other types of responses. The ones built into Arc are the following.

* TextResponse
* RedirectResponse
* Response

Arc also has support for all of Starlettes web response classes.

# Async
Arc has support for creating asynchronous routes and handlers, which can lead to better performance. Copy and paste the below code into your python file.
```py
from arc import App, TextResponse

app = App()

@app.route("/")
async def index(request):
    return TextResponse("Hello Async!")

if __name__ == "__main__":
    app.run()
```

# Deployment
Once you're done making your website, you'll probably want to deploy it. I don't suggest running the default uvicorn web server for deployment, instead you can use `guvicorn` with `UvicornWorker`. Keep in mind that `guvicorn` is only available on linux. You can use the following to deploy it.
```
gunicorn -k uvicorn.workers.UvicornWorker main:app
```
You can look at the uvicorn and gunicorn documentations on more information on this.

# Afterword
Hey, glad you made it this far, Arc is still under heavy development, and I'm still adding more features and bug fixes. If you find any bugs or problems in your code, feel free to open an issue or email me at aboominister@gmail.com. All help is appreciated. A full API reference is coming soon. Thanks :D
