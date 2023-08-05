"""
Rototiller: Coroutine Utilities.

* single-call init with `Coro.init(*args, **kwargs)` (no `coro.send(None)` needed)
* recording and printing of coroutine inputs and outputs with Recorded.
* clean, semantic output types (Yielded, Raised, Returned)
"""


# [ Imports:Python ]
import sys
import types
import typing

# [ Imports:Third Party ]
import din


# [ Exports ]
__all__ = (
    'Coro',
    'RecordedCoro',
    'Yielded',
    'Returned',
    'Raised',
    'OutputType',
    'ThrowableType',
    'WrappableObjType',
    'WrappableFuncType',
)


def __dir__() -> typing.Tuple[str, ...]:  # pragma: no cover
    return __all__


# [ Internal ]
_GenericTypeVar = typing.TypeVar('_GenericTypeVar')
_YieldTypeVar = typing.TypeVar('_YieldTypeVar')
_SendTypeVar = typing.TypeVar('_SendTypeVar')
_ReturnTypeVar = typing.TypeVar('_ReturnTypeVar')


# [ API ]
WrappableObjType = typing.Union[
    typing.Generator[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar],
    typing.Coroutine[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar],
]
WrappableFuncType = typing.Callable[..., WrappableObjType[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar]]


ThrowableType = typing.Union[
    BaseException,
    typing.Tuple[
        typing.Optional[typing.Type[BaseException]],
        typing.Optional[BaseException],
        typing.Optional[types.TracebackType],
    ],
]


class Yielded(din.ReprMixin, typing.Generic[_GenericTypeVar]):  # pylint: disable=unsubscriptable-object
    """A value yielded by a WrappableObjType."""

    def __init__(self, value: _GenericTypeVar) -> None:
        super().__init__()
        self.value = value


class Returned(din.ReprMixin, typing.Generic[_GenericTypeVar]):  # pylint: disable=unsubscriptable-object
    """A value returned by a WrappableObjType."""

    def __init__(self, value: _GenericTypeVar) -> None:
        super().__init__()
        self.value = value


class Raised(din.ReprMixin):
    """An error raised by a WrappableObjType."""

    def __init__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        exc_traceback: typing.Optional[types.TracebackType],
    ):
        super().__init__()
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback
        self.value = (self.exc_type, self.exc_value, self.exc_traceback)


OutputType = typing.Union[
    Yielded[_YieldTypeVar],
    Returned[_ReturnTypeVar],
    Raised,
]


# pylint is wrong about 'Generic' being unsubscriptable:
# https://docs.python.org/3/library/typing.html#user-defined-generic-types
# pylint: disable=unsubscriptable-object
# XXX switch to just functions that return a coro state?
class Coro(din.ReprMixin, typing.Generic[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar]):
    """
    Provides an init method on coroutines.

    `coro = Coro(func)` creates an object with an interface consistent with coroutines
    (send, throw) and adds an init.  The init is equivalent to calling the function
    to get the coroutine, then sending the initial None to that coroutine.

    `yielded = Coro(func).init(*args, **kwargs)`:
    * `coro = func(*args, **kwargs)`
    * `yielded = coro.send(None)`
    """

    def __init__(self, func: WrappableFuncType[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar]) -> None:
        super().__init__()
        self.func = func
        self.coro: WrappableObjType[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar]
        self.args: typing.Tuple[typing.Any, ...] = ()
        self.kwargs: typing.Dict[str, typing.Any] = {}

    def init(self, *args: typing.Any, **kwargs: typing.Any) -> OutputType[_YieldTypeVar, _ReturnTypeVar]:
        """Initialize the coroutine and return the first yielded value."""
        self.args = args
        self.kwargs = kwargs
        self.coro = self.func(*args, **kwargs)
        # casting the send type, because you *must* send None in first, but otherwise it's invalid,
        # and unnecessarily complicates the type signatures, and I don't want to do that.
        return self.send(typing.cast(_SendTypeVar, None))

    def send(self, value: _SendTypeVar) -> OutputType[_YieldTypeVar, _ReturnTypeVar]:
        """Send the value into the coroutine and return the value it yields."""
        try:
            return Yielded(self.coro.send(value))
        except StopIteration as return_error:
            return Returned(return_error.value)
        # intentionally capturing all
        except Exception:  # pylint: disable=broad-except
            return Raised(*sys.exc_info())

    def throw(self, throwable: ThrowableType) -> OutputType[_YieldTypeVar, _ReturnTypeVar]:
        """Throw the exception into the coroutine and return the value it yields."""
        try:
            if isinstance(throwable, tuple):
                return Yielded(self.coro.throw(*throwable))  # type: ignore
            # mypy insists the first arg must be typing.Type[BaseException], which isn't true
            return Yielded(self.coro.throw(throwable))  # type: ignore
        except StopIteration as return_error:
            return Returned(return_error.value)
        # intentionally capturing all
        except Exception:  # pylint: disable=broad-except
            return Raised(*sys.exc_info())

    def __str__(self) -> str:  # pragma: no cover
        lines = [
            f"[rototiller.Coro]",
            f"  func: {self.func.__module__}.{self.func.__qualname__}",
            f"  args:",
            *("\n".join(f"    {l}" for l in f"{a}".splitlines()) for a in self.args),
            f"  kwargs:",
            *("\n".join(f"    {l}" for l in f"{k}: {v}".splitlines()) for k, v in self.kwargs.items()),
        ]
        return "\n".join(lines)
# pylint: enable=unsubscriptable-object


class RecordedCoro(Coro[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar]):
    """
    A Coro with recorded actions (init/send/throw) and responses (yield/raise).

    Inputs and outputs are recorded, accessible via `get_history`
    """

    def __init__(self, func: WrappableFuncType[_YieldTypeVar, _SendTypeVar, _ReturnTypeVar]) -> None:
        super().__init__(func)
        self._history: typing.List[typing.Dict[str, typing.Any]] = []

    def init(self, *args: typing.Any, **kwargs: typing.Any) -> OutputType[_YieldTypeVar, _ReturnTypeVar]:
        """Initialize the coroutine and return the first yielded value."""
        output = super().init(*args, **kwargs)
        self._history.append({'args': args, 'kwargs': kwargs, 'output': output})
        return output

    def send(self, value: _SendTypeVar) -> OutputType[_YieldTypeVar, _ReturnTypeVar]:
        """Send the value into the coroutine and return the value it yields."""
        output = super().send(value)
        self._history.append({'sent': value, 'output': output})
        return output

    def throw(self, throwable: ThrowableType) -> OutputType[_YieldTypeVar, _ReturnTypeVar]:
        """Throw the exception into the coroutine and return the value it yields."""
        output = super().throw(throwable)
        self._history.append({'thrown': throwable, 'output': output})
        return output

    def _get_state_str(self) -> typing.Iterable[str]:  # pragma: no cover
        for item in tuple(self._history):
            if tuple(sorted(item.keys())) == tuple(sorted(('args', 'kwargs', 'output'))):
                yield "\n".join([
                    f"Initialized with:",
                    f"  args:",
                    *("\n".join(f"    {l}" for l in f"{a}".splitlines()) for a in item['args']),
                    f"  kwargs:",
                    *("\n".join(f"    {l}" for l in f"{k}: {v}".splitlines()) for k, v in item['kwargs'].items()),
                    f"  output: {item['output']}",
                ])
            elif tuple(sorted(item.keys())) == tuple(sorted(('sent', 'output'))):
                yield "\n".join([
                    f"Sent:",
                    f"  value: {item['sent']}",
                    f"  output: {item['output']}",
                ])
            elif tuple(sorted(item.keys())) == tuple(sorted(('thrown', 'output'))):
                yield "\n".join([
                    f"Thrown:",
                    f"  error: {item['thrown']!r}",
                    f"  output: {item['output']}",
                ])
            else:
                raise RuntimeError(f"Cannot stringify: unrecognized item in history ({item})")

    def __str__(self) -> str:  # pragma: no cover
        lines = [
            f"[rototiller.Restorable]",
            f"  func: {self.func.__module__}.{self.func.__qualname__}",
            f"  history:",
            *("\n".join(f"    {l}" for l in f"{s}".splitlines()) for s in self._get_state_str()),
        ]
        return "\n".join(lines)


# [ Vulture ]
# pylint: disable=pointless-statement
# These are all API's, and called in the tests, at least
RecordedCoro
