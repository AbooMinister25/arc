# Tutorial: SimpleAPI


In this tutorial, we'll be creating a simple API that'll be used to return a joke in the form of JSON. The API will take advantage of Arc's `JSON` response class that uses `orjson` to quickly return the JSON data. Alright, lets delve a bit more into what exactly our API is going to do. We're going to have three routes, `/getjoke`, `/submitjoke`, and `/alljokes`. The first one is simple, it'll return a single joke from our JSON database. The second will allow the users to submit their own jokes, and the last will be used to return our entire store of jokes. Lets get started. First, create a new directory called `jokesapi`. Navigate inside the directory and create a `main.py` file, this file will contain all of our code for the API. Once your done, your directory structure should look something like this.

```
jokesapi/
    main.py
```

Once you have that, open the `main.py` file, and put the following code inside of it.

```py
from arc import App, TextResponse

app = App()

@app.route("/")
def index(request):
    return TextResponse("Jokes API")

if __name__ == "__main__":
    app.run()
```

Alright, the above is pretty straightforward, we're importing and initializning our application and returning a simple response in the form of text. Now, run the app to make sure our code is working correcly. You should see something like the following.

```
INFO: Running on http://127.0.0.1:5000

INFO: Press CTRL + C to stop
```

Alright, lets start adding our routes. Change your code so it looks like the following.

```py
from arc import App, JSON

app = App()

@app.route("/getjoke")
def getjoke(request):
    ...

if __name__ == "__main__":
    app.run()
```

Lets break this down. what we've done above is import a new class, the `JSON` class, which we will be using to send our data. We then declared the `/getjoke` route, with an empty handler. Now, don't run your application just yet, we have to finish coding the handler first. We'll need a JSON file that contains our jokes. For that, create a new file in your `jokesapi` directory, `jokes.json`. Once you've done that, your file tree should look something like this.

```
jokesapi/
    main.py
    jokes.json
```

Open up `jokes.json` and put [this](https://gist.github.com/AbooMinister25/6c8f4b9e19f4071b74de11856d887cb4) JSON data into it. Once you've done that, navigate back to your python file and update it so it looks like this.

```py
from arc import App, JSON
import orjson
import random

app = App()

jokes = orjson.loads(open("jokes.json", "r").read())

@app.route("/getjoke")
def getjoke(request):
    joke = random.choice(jokes)
    return JSON(joke)

if __name__ == "__main__":
    app.run()
```

Alright, what the above is doing is importing the `orjson` and `random` modules, you should already have `orjson` installed since it came with `Arc`, but if you don't, go ahead and do

```
pip install orjson
```

We're then taking the `orjson` module, and using its `.load()` method to open and read the contents of our `jokes.json` file and store it into the `jokes` variable. We then take that and use `random.choice()` to get a random joke from the `jokes` variable and return it as `JSON` using the `JSON` class. Now, run your app, and head to [http://127.0.0.1:5000/getjoke](http://127.0.0.1:5000/getjoke) to see your app in action. Each time you refresh it, a different joke should come up. Now lets add the `/submitjoke` route. Change your code so it looks like the following.

```py
from arc import App, JSON
import orjson
import random

app = App()

jokes = orjson.loads(open("jokes.json", "r").read())

@app.route("/getjoke")
def getjoke(request):
    joke = random.choice(jokes)

    return JSON(joke)

@app.route("/submitjoke/{joke}")
def submitjoke(request, joke):
    if request.method == "POST":
        joke = orjson.loads(joke)
        
        jokes.append(joke)

        with open("jokes.json", "w") as jokes_file:
            jokes_file.write(jokes)

if __name__ == "__main__":
    app.run()
```