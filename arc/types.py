from typing import Callable, Any, Awaitable, TypeVar

CoroutineFunction = Callable[[Any], Awaitable]
DCallable = TypeVar("DCallable", bound=Callable)
