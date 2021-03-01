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

Now, head to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see your app in action.