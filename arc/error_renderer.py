from typing import Optional

TRACEBACK_STYLE = """
pre code {
  background-color: #c8ccd4;
  word-wrap: break-word;
  box-decoration-break: clone;
  padding: .1rem .3rem .2rem;
  border-radius: .2rem;
    white-space: nowrap;
}
"""

HTML_ERROR_TEMPLATE = """
<html> 
    <head>
        <title> Error {error_code} </title>
        <style> {style} </style>
    </head>
    <h1> Error {error_code} </h1>
    <p>{error_label}</p>
    <h2> Traceback </h2>
    <pre><code>
        {traceback}
    </code></pre>
    <h2> Request Info </h2>
    <div class="request">
        <p> Method </p> {method}
        <p> URL </p> {url}
        <p> Exception </p> {exception}
        <p> Python Version </p> {python_v}
        <p> Arc Version </p> {arc_v}
        <p> Error Source </p> {source}
        <p> Headers </p> {headers}
    </div>
    <p> 
    Traceback and request info is shown due to <code>DEBUG=True</code> enabled in your app settings. 
    Make sure to turn this off for production 
    </p>
</html>
"""


class ErrorRenderer:
    """Renders exceptions as either HTML, JSON, or text.

    Used to render errors that the Arc app may encounter. Can use
    either HTML, JSON, or plain text. Defaults to HTML.

    Args:
        exception: The exception that was raised.
        request_info: A dictionary of information about the request.
        render_format: The format in which the error is rendered.
          defaults to HTML.
        error_code: The error code to use. Defaults to 500.
        error_label: A message to use as a label to the error.

    """

    def __init__(
        self,
        exception: Exception,
        request_info: dict[str],
        render_format: Optional[str] = "html",
        error_code: Optional[int] = 500,
        error_label: Optional[str] = "An error occurred in your application",
    ):
        ...
