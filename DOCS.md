# Arc Documentation

### Arc is a python micro web framework designed for creating dynamic web applications.

# Contents
* [Installation](#Installation)
* [Quickstart](#Quickstart)
* [Routes](#Routes)
* [Templates](#Templates)
* [Sessions/Cookies](#Sessions/Cookies)
* [Middleware](#Middleware)
* [Collections](#Collections)



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
from arc import App

app = App()

@app.route("/")
def home(req, res):
    res.text = "Hello, World"

if __name__ == "__main__": 
    app.run()
```
Alright, lets break this code down. Arc has a single `App` module that you need to import in order to create your web app. The `App` module has all of the methods that you'll need in order to create a basic web application. Once you initialize the `App` module, you can then use a decorator to define a route. You can than define a function to be the handler that is called when that route is invoked. Lastly, we check if the file is being run directly, and run our web application. Now, run the code you just copy and pasted, once you've done that, you should see something like the below in your console.
```
[INFO] Running on http://127.0.0.1:5000
[INFO] Press CTRL + C to stop
```
Don't worry if you see the below warning.
```
C:\Users\aboom\AppData\Local\Programs\Python\Python38\lib\site-packages\whitenoise\base.py:115: UserWarning: No directory at: D:\Projects\Test\static\
  warnings.warn(u"No directory at: {}".format(root))
```
Great, you've successfully run your web application! Head over to http://127.0.0.1:5000 to see your web application in action. Once you're there, you should see the text `Hello World` displayed on the screen.

# Routes
If you've used a web framework before, you know that you have to define routes in your application. Routes are sort of like highways that send requests to the code that handles them. In Arc, there are two ways you can create routes, one of which uses decorators, similar to Flask and Bottle, and the other takes inspiration from Django. Below is how you can create routes using decorators.
```py
from arc import App

app = App()

@app.route("/home")
def home(req, res):
    res.text = "Welcome to the home page"

@app.route("/")
def index(req, res):
    res.text = "Go to http://localhost:5000/home to see the home page"

if __name__ == "__main__":
    app.run()
```
The above code is signifying two different routes. One of which is `/home`, which executes the code in the `home()` function defined here. Another specifies the `/` route, which is just http://localhost:5000. If you prefer a more Django like routing style, you can do the below.
```py
from arc import App

app = App()

def home(req, res):
    res.text = "Welcome to the home page"

def index(req, res):
    res.text = "Go to http://localhost:5000/home to see the home page"

app.add_route("/home", home)
app.add_route("/", index)

if __name__ == "__main__":
    app.run()
```
The above does the exact same thing as the first example with decorators, but instead of a decorator based routing system, we're using the `App` class's `.add_route` method. Now lets take a closer look at the handlers. A basic handler is structured as the following.
```py
def handler_name(req, res):
    # handler code
```
You have a function name, which you can define as anything you want, two parameteres, which represent `request` and `response`, and the contents of the handler, which decide what to do. Adding content to the web pages uses the `response` parameter, where you can declare to body or the text of the web page. You can use the `req` parameter to see whether the request is a `GET` or `POST` request, among other things. Arc also supports class based handlers, as per the following.
```py
from arc import App

app = App()

@app.route("/classhandler")
class ClassHandler:
    def get(self, req, res):
        res.text = "You issued a GET request"
    
    def post(self, req, res):
        res.text = "You issued a POST request"
```
Using class based handlers makes it easier to specify what happens when you issue different types of requests.

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
from arc import App

app = App()

@app.route("/")
def index(req, res):
    res.body = app.template("index.html", context={"title": "Arc Templates", "heading": "Arc is AMAZING!"})

if __name__ == "__main__":
    app.run()
```
Once you have that, run your file and head to http://127.0.0.1:5000 to see your web page in action. Once you're there, you should see the text `Arc is AMAZING` on the screen. Now, lets break down what we've done here. We used the `app.template` method of our `App` class to define a template. In this function, you have to provide a template name, and context, which we provided as a dictionary. Jinja2 will then use the corresponding `title` and `heading` values to fill out the variables we put in the HTML page. Keep in mind that you should use `res.body` instead of `res.text` to define a web page. By default, jinja2 searches for templates in the `templates` folder, but you can change that when initializing the `App` class like the following.
```py
from arc import App

app = App(templates_dir="pages")
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

# Sessions/Cookies
Arc has support for creating sessions, as well as cookies. Sessions are data that you can store, and which expire once the browser is closed. Copy and paste the below code into your python file.
```py
from arc import App, Session

app = App()
session = Session(app)

@app.route("/")
def setsession(req, res):
    res.text = "Storing Session"
    session.make_session("Data", "Arc Is AMAZING", res)

@app.route("/getsession")
def getsession(req, res):
    res.text = session["Data"]

if __name__ == "__main__":
    app.run()
```
Lets break this down. As you may have noticed, we imported another class, the `Session` class, which is used for creating and storing sessions. It takes `app` as an argument. The `Session` class behaves sort of like a dictionary, and data is stored in key/value pairs. Now run the code you just copied, and head to http://127.0.0.1:5000. Once you've head there, head to http://127.0.0.1:5000/getsession. Once you've done that, the text `Arc is AMAZING` should show up on screen. Keep in mind that if you head to the `/getsession` route before the `/` route, this code will raise an error, as the session key `Data` has not yet been created. By default, sessions expire when you close the webpage, but you can change that as per the following.
```py
from arc import App, Session
import datetime

app = App()
session = Session(app, lifetime=datetime.timedelta(minutes=60))

@app.route("/")
def setsession(req, res):
    session.make_session("test", "test", res)
    res.text = "Making Session"

@app.route("/getsession")
def getsession(req, res):
    res.text = session["test"]
```
Keep in mind that changing session lifetimes is still being worked on, if you encounter any problems, please let me know by opening up an issue. Now lets look at cookies. Cookies can be created using the `App` class's `.set_cookie()` method.
You can retrieve cookies using both the `.get_cookies()` and `.get_cookie()` methods. Now, copy and paste the example below.
```py
from arc import App

app = App()

@app.route("/")
def setcookie(req, res):
    app.set_cookie("data", "arc is great, isn't it", res)
    res.text = "Setting Cookie"

@app.route("/getcookie")
def getcookie(req, res):
    # Getting all cookies
    all_cookies = app.get_cookies(req)

    # Getting a specific cookie
    cookie = app.get_cookie(req, "data")

    res.text = f"All Cookies: {all_cookies}, Data: {cookie}"
```
Alright, the above code is doing three things, setting a cookie with the key `data`, getting all of the stored cookies, and getting just the `data` cookie.
The `.get_cookies()` function gets all of the cookies stored, and `.get_cookie()` takes a `key` argument and gives the corresponding data. As with sessions, you can provide custom lifetimes to the cookies using the `datetime` module.
```py
from arc import App

app = App()

@app.route("/")
def setcookie(req, res):
    app.set_cookie("data", "arc is great, isn't it", res,                       lifetime=datetime.timedelta(minutes=10))

    res.text = "Setting Cookie"

@app.route("/getcookie")
def getcookie(req, res):
    res.text = app.get_cookie("data")
```
Again, setting custom lifetimes is still experimental, and may have some problems, so make sure to open an issue.

# Middleware
Arc has support for adding custom middleware. If you don't know what it is, middleware is basically a component that you can use to modify the behavior of an incoming request or an outgoing response. By default, Arc has a middleware created that logs requests and responses onto the console. You may have noticed this, as each time you make a request, it's logged in the console, alongside the outgoing response. In order to make custom middlewares, you have to use Arc's `Middleware` class. Copy the following code into your python file.
```py
from arc import App, Middleware

app = App()

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
Lets break this down. As you may have noticed, we imported the `Middleware` class to help us construct our custom middleware. Then we created the `CustomMiddleware`
class which consists of the `process_request()` and `process_response()` methods. These methods decide what to do in order to handle a response or request, in our case, they are printing to the console each time a request is made or a response is given. Now lets run our code. Head to http://127.0.0.1:5000, and back to your code. Something like below should have appeared.
```
[INFO] Running on http://127.0.0.1:5000
[INFO] Press CTRL + C to stop

Recieved a request
[REQUEST][GET] http://127.0.0.1:5000/

[RESPONSE] http://127.0.0.1:5000/
Sent a response
```
Congratulations, your custom middleware worked. Now, above, we have two middlewares at work here, the default one, and our custom one. In some cases, we may not want the default middleware clogging up the console if we have our own custom one running, because of this, you can disable the default middleware. In order to do this, edit your current code so it looks like the following.
```py
from arc import App, Middleware

app = App(default_middleware=False)

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
from arc import Collection

mycollection = Collection()

@mycollection.route("/")
def index(req, res):
    res.text = "Collections are cool!"
```
As you can see above, a collection behaves almost exactly like the main app class, and has most of the same methods, and the ability to serve HTML templates and create cookies, so you're not losing anything by using a collection. Alright, lets test this out, run your `__init__.py` file and head to http://127.0.0.1:5000 to see your app in action.

# Afterword
Hey, glad you made it this far, Arc is still under heavy development, and I'm still adding more features and bug fixes. If you find any bugs or problems in your code, feel free to open an issue or email me at aboominister@gmail.com. All help is appreciated. A full API reference is coming soon. Thanks :D
