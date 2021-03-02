# Deployment

Once you're done making your website, you'll probably want to deploy it. I don't suggest running the default uvicorn web server for deployment, instead you can use `guvicorn` with `UvicornWorker`. Keep in mind that `guvicorn` is only available on linux. You can use the following to deploy it.

```
gunicorn -k uvicorn.workers.UvicornWorker --reload main:app
```
You can look at the uvicorn and gunicorn documentations on more information on this.