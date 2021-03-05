# Arc 2.4.29### Python ASGI web framework for creating fast and dynamic web applications.

Arc is a python ASGI web framework for creating dynamic web pages. Arc is still under heavy devlopment, and all help is appreciated. Arc is built using `Starlette`, and runs on the lighting fast `uvicorn` web server.

## Installation
Arc is relatively easy to get set up with. Arc is cross platform, and can be installed on any operating system. You can install it using pip.
```
# Windows
pip install arcframework

# Linux
pip3 install arcframework
```

## Quickstart
Arc is a very easy to use libary, and is similar to other micro frameworks such as Flask or Bottle, so learning it won't be too hard. The below is an example of an Arc application.
```py
from arc import App, TextResponse

app = App()

@app.route("/home")
def home(request):
    return TextResponse("Hello, World")

if __name__ == "__main__":
    app.run()
```
Copy and paste the above and run your file, you'll get an output like the following in your console.
```
INFO: Running on http://127.0.0.1:5000

INFO: Press CTRL + C to stop
```
Now go to http://127.0.0.1:5000/home, and you should see `Hello World` being displayed on the screen.

## Issues/Bugs
Arc is still under heavy development abd has loads of bugs and errors that I'm constantly working on resolving. You can check out the documentation at https://aboominister25.github.io/arc/. Feel free to open an issue or email me at aboominister@gmail.com, all help would be appreciated.