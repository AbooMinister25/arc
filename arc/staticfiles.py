from starlette.responses import Response
import os
import mimetypes


class EmptyWSGI:
    def __init__(self):
        ...


class StaticFile:
    def __init__(self, directory):
        self.directory = directory
    
    def __call__(self, request, filename: str):
        headers = {}
        path = os.path.relpath(filename, os.getcwd())
        
        with open(f"{self.directory}/{path}", "rb") as f:
            data = f.read()
        
        mimetype = mimetypes.guess_type(filename)
        
        headers.update(
            {
                "Content-Type": mimetype
            }
        )
        
        return Response(data, media_type=mimetype[0])


