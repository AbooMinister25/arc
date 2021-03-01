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

As you can see above, a collection behaves almost exactly like the main app class, and has most of the same methods, and the ability to serve HTML templates and create cookies, so you're not losing anything by using a collection. Alright, lets test this out, run your `__init__.py` file and head to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see your app in action.
