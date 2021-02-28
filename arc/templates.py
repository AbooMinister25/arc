from jinja2 import Environment, FileSystemLoader
from starlette.responses import Response
import jinja2
import typing


class Template:
    def __init__(self, directory: str = "templates") -> None:
        self.env = self.get_env(directory)

    def get_env(self, directory: str) -> "Environment":
        @jinja2.contextfunction
        def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
            request = context["request"]
            return request.url_for(name, **path_params)

        loader = FileSystemLoader(directory)
        env = jinja2.Environment(loader=loader, autoescape=True)

        env.globals["url_for"] = url_for

        return env

    def get_template(self, name: str) -> "jinja2.Template":
        return self.env.get_template(name)

    def __call__(self, name: str, context: dict, status_code: int = 200, headers: dict = None, media_type: str = None) -> Response:
        if "request" not in context:
            raise ValueError('Context must include a "request" key')

        template = self.env.get_template(name)

        return Response(
            template.render(context),
            status_code=status_code,
            headers=headers,
            media_type=media_type
        )
