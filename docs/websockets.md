# Websockets

Like any good framework, Arc has full support for creating and using websockets. If you don't know what a websocket is, its basically a way for your frontend to communicate with your backend. So if you have javascript frontend code, you can use websockets to communicate your python backend with your javascript frontend. This can be extremely useful, and Arc makes websockets easy and very straightforward to use. Arc's websockets integration uses Starlettes `WebSocket` class. Below is a basic example using websockets in Arc.

```py
from arc import App, HTML

app = App()

@app.route("/")
async def index(request):
    return HTML(
"""
<!DOCTYPE html>
<html>
    <head>
        <title> Websockets :D </title>
    </head>
    <body>
        <h1> Type in a message below </h1>
        <form action="" onsubmit="displayMessage(event)">
            <input type="text" id="messageText" autocomplete="off" />
            <button>Display</button>
        </form>
        <ul id="messages"></ul>

        <script>
            var ws = new WebSocket("ws://localhost:5000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function displayMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
    )

@app.websocket("/ws")
async def test_websocket(websocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You entered: {data}")

if __name__ == "__main__":
    app.run()
```

Alright, thats a lot to take in, so lets break it down. So, as you may have noticed, alongside our `App` class, we imported the `HTML` class, which is used for rendering responses in the form of html. We then rendered an HTML page that has a text box for you to enter text, and a submit button. We also have some javascript code that connects to our websocket and provides functions on what to do when it recieves a message, and when the text box form is submitted. We then used a new type of function from `Arc`, the `app.websocket` method, which is used to create websockets, and requires a default `websocket` argument. Keep in mind that websocket handlers always have to be asynchronous. So what our websocket handler is doing is waiting for a message, and sending back that message to the frontend for the js to load into the html page. Now, lets run our app and head to [http://127.0.0.1:5000](http://127.0.0.1:5000). Once you're there, type in the text box that should have appeared and click the `Display` button, and if everything went well, the words you just typed into the text box should appear onto the screen. Now, you may not want to have your HTML inside your python file, so lets clean that up and render it using a jinja2 template.

```py
from arc import App, Template

app = App()
template = Template()

@app.route("/")
async def index(request):
    return template("index.html", context={"request": request})

@app.websocket("/ws")
async def test_websocket(websocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You entered: {data}")

if __name__ == "__main__":
    app.run()`
```

create a directory called `templates` and put an `index.html` file with the following contents inside of it.

```html
<!DOCTYPE html>
<html>
    <head>
        <title> Websockets :D </title>
    </head>
    <body>
        <h1> Type in a message below </h1>
        <form action="" onsubmit="displayMessage(event)">
            <input type="text" id="messageText" autocomplete="off" />
            <button>Display</button>
        </form>
        <ul id="messages"></ul>

        <script>
            var ws = new WebSocket("ws://localhost:5000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function displayMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
```

Once you've done that, run your app, head back to [http://127.0.0.1:5000](http://127.0.0.1:5000) and watch your app in action. As I mentioned earlier, Arc uses Starlettes `WebSocket` class to handle websockets, so check out Starlettes documentation on their `WebSocket` class for more information on what websockets can do [https://www.starlette.io/websockets/](https://www.starlette.io/websockets/). You can check out [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) on more information for the frontend side in the javascript.