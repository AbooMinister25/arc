from typing import Mapping, Union, Any, Optional


class Headers:
    """Multidict storing HTTP headers

    Stores http headers in a key-value format. Allows for multiple
    values for every key. Keys and values are encoded in latin-1.

    Args:
        values: A mapping or a list of tuples containing the
          default headers.
    """

    def __init__(self, values: Union[Mapping[str, str], list[tuple[bytes, bytes]]]):
        if values:
            _items = list(values.items()) if hasattr(values, "items") else list(values)
        else:
            _items = []

        self._list = [
            (key.lower().encode("latin-1"), value.lower().encode("latin-1"))
            for key, value in _items
        ]

    def keys(self) -> list[str]:
        return [key.decode("latin-1") for key, _ in self._list]

    def items(self) -> list[tuple[str, str]]:
        return [(k.decode("latin-1"), v.decode("latin-1")) for k, v in self._list]

    def values(self) -> list[str]:
        return [value.decode("latin-1") for value, _ in self._list]

    def __getitem__(self, key: str) -> str:
        for k, v in self._list:
            if k.lower() == key.lower().encode("latin-1"):
                return v.decode("latin-1")

        raise KeyError(key)

    def get(self, key: str, default: Optional[Any] = None) -> str:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Headers):
            return False

        return self._list == other._list

    def __contains__(self, key: str) -> bool:
        for k, v in self._list:
            if k.lower() == key.lower().encode("latin-1"):
                return True

        return False
