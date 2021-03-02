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
from arc import App, Template

app = App()

template = Template()

@app.route("/")
def index(request):
    return template("index.html", context={"request": request, "title": "Templates", "heading": "Arc is AMAZING"})

if __name__ == "__main__":
    app.run()
```

Once you have that, run your file and head to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see your web page in action. Once you're there, you should see the text `Arc is AMAZING` on the screen. Now, lets break down what we've done here. Instead of importing `TextResponse` like before, we used Arc's `Template` class. The `Template` class behaves just like a response, and requires you to fill out a template name, and the context, which is a dict. You are required to provide `request` to the context as a key. By default, the `Template` class searches for templates in the `templates` directory, but you can change that by doing the following.

```py
from arc import App, Template

app = App()
template = Template(directory="pages")
```
If you do the above, arc will then search for templates in the `pages` directory.