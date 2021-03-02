# Static Files

Whats a good web page without decent styling? Luckily for us, `Arc` has support for serving static files. First, lets create a directory called `static` in our current working folder. Inside the new `static` folder, create a `style.css` file and put the following code in it.

```css
body {
    background-color: orange;
}
```

Now, create an `index.html` file and put the following code into it.

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

Now, put the following code into your main python file.

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

Alright, now that you're done with that, run your python file and head to [http://127.0.0.1:5000](http://127.0.0.1:5000). Once you're there, the background of the page should now be orange. Similarly to how you can change the default `templates` folder, you can also change the default `static` folder to something else like below.

```py
from arc import App

app = App(static_dir="styles")
```
Now, the code will serve static files from the `styles` directory.