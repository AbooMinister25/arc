# Forms

Say you have an HTML page that has a form in it, how would you process that data? Luckily, Arc has a built in way to process form data. First, open a python file and put the below code into it.

```py
from arc import App, Form, Redirect, Template

app = App()

template = Template()

@app.route("/")
async def index(request):
    if "data" not in request.query_params:
        data = None
    else:
        data = Form(request.query_params["data"]) 

    return template("index.html", context={"request": request, "data": data})

@app.route("/submitdata", methods=["POST"])
async def submitdata(request):
    body = await request.body()
    form = Form(body)
    return Redirect(f"/?data={form.data}")

if __name__ == "__main__":
    app.run()
```

Next, open a new HTML file in a `templates` directory and put the below code into it.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Forms :D</title>
  </head>
  <body>
    <h1>Type in a message below</h1>
    <form action="/submitdata"method="post">
      <input type="text" id="messageText" name="message" autocomplete="off" />
      <button>Display</button>
    </form>
    {% if data is not none %}
    <h1>{{data["message"]}}</h1>
    {% endif %}
  </body>
</html>
```

Alright, now lets break down what we did, starting with the python. As you may have noticed, we imported a new class into our code, the `Form` class, which is used to render form data in a dict like object from the requests body. We created two routes, a `/` route, and a `/submitdata` routes. The latter only accepts POST requests, because thats where we'll be submitting our form data to. In the first route, we're checking whether `data` is in the query parameters of the request. We then return the template with the context filled in. In our second route, we handle the form data. Make sure your second route is asynchronous, as we're awaiting the request body. After we have the body, we used the `Form` class to get the form data in a dict like object. We then redirected to our `/` route, and provided `data` as one of the query parameters. Now, run your application and head to [http://127.0.0.1:5000](http://127.0.0.1:5000), and enter a message in the text box and submit it, and you should see your entered message on the screen. Now, we used two routes in this example, but you can also use one route instead. Change your python file so it looks like the below.

```py
from arc import App, Form, Redirect, Template

app = App()

template = Template()

@app.route("/", methods=["GET", "POST"])
async def index(request):
    if request.method == "GET":
        data = None
        
        return template("notindex.html", context={"request": request, "data": data})
    
    elif request.method == "POST":
        body = await request.body()
        form = Form(body)

        return template("notindex.html", context={"request": request, "data": form.data})
    

if __name__ == "__main__":
    app.run()
```

Change your HTML to look like this

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Form :D</title>
  </head>
  <body>
    <h1>Type in a message below</h1>
    <form action=""method="post">
      <input type="text" id="messageText" name="message" autocomplete="off" />
      <button>Display</button>
    </form>
    {% if data is not none %}
    <h1>{{data["username"]}}</h1>
    {% else %}
    <h1>Data is None</h1>
    {% endif %}
  </body>
</html>
```

Once you've done that, run your application, enter something into the text box, and if you've done everything correctly, the message you've entered should appear on the screen.