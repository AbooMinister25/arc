# Class Based Routing

Arc has the ability to use class based routing in your application. Class based routing allows you to take the `App` class and inherit it in your own class, and lets you define routes from withing the class, which can make your code more organized. To get started, open a python file and place the below into your code.

```py
from arc import App, TextResponse

class MyCustomApplication(App):
    def __init__(self):
        super().__init__() # Init parameters for the App class can go here

        self.routes = {
            "/": self.index,
            "/home": self.home,
            "/about": self.about
        }
    
    async def index(self, request):
        return TextResponse("Welcome! You can head to http://127.0.0.1:5000/home to go to the home page, and to http://127.0.0.1:5000/about to go to the about page.")
    
    async def home(self, request):
        return TextResponse("Welcome to the home page!")
    
    async def about(self, request):
        return TextResponse("Welcome to the about page!")

app = MyCustomApplication()

if __name__ == "__main__":
    app.run()
```

Now, lets break the above down. We're importing the `App` class from Arc and using it as a base class in our custom application. We then called the `App` class's `__init__` method, which can be supplied all the normal arguments. We then defined a dictionary called `routes`, which the `App` class uses to define a handler for each route. We also created three methods inside our class, `index`, `home`, and `about`, and each of them are used to handle our applications routes. Our custom application has all the methods and features that the `App` class provides, and allows you to define your own. Now, run your application and head to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see your app in action. You can visit each of the routes to see what happens. Now, if you want to provide additional options for each of the routes, like the `methods` option in the decorator method, you can do the below.

```py
from arc import App, TextResponse

class MyCustomApplication(App):
    def __init__(self):
        super().__init__() # Init parameters for the App class can go here

        self.routes = {
            "/": {"handler": self.index, "methods": ["GET"]},
            "/home": self.home,
            "/about": self.about,
        }
    
    async def index(self, request):
        return TextResponse("Welcome! You can head to http://127.0.0.1:5000/home to go to the home page, and to http://127.0.0.1:5000/about to go to the about page.")
    
    async def home(self, request):
        return TextResponse("Welcome to the home page!")
    
    async def about(self, request):
        return TextResponse("Welcome to the about page!")

app = MyCustomApplication()

if __name__ == "__main__":
    app.run()
```

Now, when you run your application, if you try to access the `/` route with a method other than `GET`, you'll be greeted with an error. Now, lets say you're using collections in your application, luckliy, `Arc` allows you to use class based handling with collections as well. Now, create a new python file and put the following code into it.

```py
from arc import Collection, TextResponse

class MyCollection(Collection):
    def __init__(self):
        super().__init__()
        
        self.routes = {
            "/register": self.register
        }
    
    async def register(self, request):
        return TextResponse("Welcome to the register page!")

mycollection = MyCollection()
```

Once you've done that, head to your main python file and change it so it looks like this.

```py
from arc import App, TextResponse
from .collectionfile import mycollection # Replace this with the name of your other python file

class MyCustomApplication(App):
    def __init__(self):
        super().__init__() # Init parameters for the App class can go here

        self.routes = {
            "/": self.index,
            "/home": self.home,
            "/about": self.about
        }
    
    async def index(self, request):
        return TextResponse("Welcome! You can head to http://127.0.0.1:5000/home to go to the home page, and to http://127.0.0.1:5000/about to go to the about page.")
    
    async def home(self, request):
        return TextResponse("Welcome to the home page!")
    
    async def about(self, request):
        return TextResponse("Welcome to the about page!")

app = MyCustomApplication()

app.register_collection(mycollection)

if __name__ == "__main__":
    app.run()
```

Now, run your app and head to [http://127.0.0.1:5000/register](http://127.0.0.1:5000:/register) and you should see your collection in action.