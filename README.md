# Arc 1.5.0
### Python micro web framework for creating dynamic websites.

Arc is a python micro framework for creating dynamic web pages. Arc is still under heavy devlopment, and only has support for basic jinja templating and static file serving at the moment. Arc is powered by a CherryPy web server, making it both fast and reliable. You can use any WSGI web server to run an Arc application.

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
from arc import App

app = App()

@app.route("/home")
def home(req, res):
    res.text = "Hello, World"

if __name__ == "__main__":
    app.run()
```
Copy and paste the above and run your file, you'll get an output like the following in your console.
```
[INFO] Running on http://127.0.0.1:5000
[INFO] Press CTRL + C to stop
```
Now go to http://127.0.0.1:5000/home, and you should see `Hello World` being displayed on the screen.

## Issues/Bugs
Arc is still under heavy development, and I do not recommend you using it in actual production until its finished. Arc has loads of bugs and errors I'm constantly working on resolving. You can check out the documentation at DOCS.md. Feel free to open an issue or email me at aboominister@gmail.com, all help would be appreciated.