from app import App


app = App(templates_dir=r"arc\templates", static_dir=r"arc\static")


@app.route("/home")
def home(request, response):
    raise Exception("ERROR")


@app.route("/hello/{name}")
def test(request, response, name):
    response.text = f"Hello, {name}"


@app.route('/testclass')
class ClassHandler:
    def get(self, req, res):
        res.text = "Get Method"

    def post(self, req, res):
        res.text = "Post Method"


def alternative(req, resp):
    resp.text = "TEST FOR ALTERNATIVE"


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={
                             "name": "test", "title": "testtitle"})


app.add_route("/testalt", alternative)


if __name__ == "__main__":
    app.run()
