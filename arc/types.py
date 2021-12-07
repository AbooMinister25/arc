from typing import Any, Awaitable, Callable, TypeVar

CoroutineFunction = Callable[[Any], Awaitable]
DCallable = TypeVar("DCallable", bound=Callable)
