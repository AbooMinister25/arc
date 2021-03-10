import orjson


class Form:
    def __init__(self, body):
        self.body = body

        try:
            self.data = self._getjson(
                body.decode() if isinstance(body, bytes) else body
            )
        except:
            self.data = self._parse_str(self.body)

    def _getjson(self, data):
        data = data.split("&")

        parsed_json = {}

        for i in data:
            i = i.split("=")
            parsed_json[i[0]] = i[1]
        
        try:
            return orjson.loads(parsed_json)
        except:
            return parsed_json

    def _parse_str(self, data):
        return orjson.loads(data.replace("'", '"'))

    def __getitem__(self, key):
        return self.data[key]
