from app import App


app = App()


@app.route("/home")
def home(request, response):
    response.text = "Hello, World"


@app.route("/hello/{name}")
def test(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/home")
def home(request, response):
    response.text = "Hello World TWO"


if __name__ == "__main__":
    app.run()
