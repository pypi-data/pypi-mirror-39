"""
Seedflow.

Side Effects As Data -> SEAD -> Seed.
Flow, because the library supports muliple concurrent flows of logic/side-effects.
"""


# [ Imports:Python ]
import abc
import functools
import inspect
import sys
import types
import typing

# [ Imports:Third Party ]
import din
import rototiller
import typing_extensions


# [ Exports ]
# XXX add tests for exports


# [ Internal ]
_GenericTypeVar = typing.TypeVar('_GenericTypeVar')
_ReturnTypeVar = typing.TypeVar('_ReturnTypeVar')
_ExcInfoType = typing.Tuple[
    typing.Optional[typing.Type[BaseException]],
    typing.Optional[BaseException],
    typing.Optional[types.TracebackType],
]
_TaskCoroType = rototiller.Coro['_Task[typing.Any]', typing.Any, _ReturnTypeVar]
_TaskFuncType = rototiller.WrappableFuncType['_Task[typing.Any]', typing.Any, _ReturnTypeVar]
_SyncFuncType = typing.Callable[..., _ReturnTypeVar]


class _ResponderProtocol(typing_extensions.Protocol[_ReturnTypeVar]):
    """A protocol describing the call signature of a function responding to coro output."""

    @abc.abstractmethod
    def __call__(
        self,
        coro: _TaskCoroType[_ReturnTypeVar],
        *,
        coro_input: typing.Any,
    ) -> rototiller.OutputType['_Task[typing.Any]', _ReturnTypeVar]:  # pragma: no coverage
        """Respond to coro output."""
        raise NotImplementedError


# pylint is wrong about typing.Generic
class _Task(din.ReprMixin, din.FrozenMixin, din.EqualityMixin, typing.Generic[_ReturnTypeVar]):  # pylint: disable=unsubscriptable-object
    """The base task that the seedflow runner executes."""

    def __init__(
        self,
        func: typing.Union[_TaskFuncType[_ReturnTypeVar], _SyncFuncType[_ReturnTypeVar]],
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        with self._thawed():
            super().__init__()
            self.func = func
            self.args = args
            self.kwargs = kwargs

    def __str__(self) -> str:  # pragma: no cover
        lines = [
            f"[seedflow._Task]",
            f"  func: {self.func.__module__}.{self.func.__qualname__}",
            f"  args:",
            *("\n".join(f"    {l}" for l in f"{a}".splitlines()) for a in self.args),
            f"  kwargs:",
            *("\n".join(f"    {l}" for l in f"{k}: {v}".splitlines()) for k, v in self.kwargs.items()),
        ]
        return "\n".join(lines)


def _strip_traceback(
    traceback: typing.Optional[types.TracebackType],
) -> typing.Optional[types.TracebackType]:
    while traceback and traceback.tb_frame.f_globals['__name__'] in (__name__, 'rototiller'):
        traceback = traceback.tb_next
    if traceback:
        traceback.tb_next = _strip_traceback(traceback.tb_next)
    return traceback


def _coro_init(
    coro: _TaskCoroType[_ReturnTypeVar], *,
    coro_input: typing.Tuple[typing.Tuple[typing.Any, ...], typing.Dict[str, typing.Any]],
) -> rototiller.OutputType[_Task[typing.Any], _ReturnTypeVar]:
    args, kwargs = coro_input
    return coro.init(*args, **kwargs)


def _coro_send(
    coro: _TaskCoroType[_ReturnTypeVar], *,
    coro_input: _GenericTypeVar,
) -> rototiller.OutputType[_Task[typing.Any], _ReturnTypeVar]:
    return coro.send(coro_input)


def _coro_throw(
    coro: _TaskCoroType[_ReturnTypeVar], *,
    coro_input: _ExcInfoType,
) -> rototiller.OutputType[_Task[typing.Any], _ReturnTypeVar]:
    return coro.throw(coro_input)


class _Return(typing.Generic[_ReturnTypeVar]):  # pylint: disable=unsubscriptable-object
    """Data type for indicating that a value should be returned."""

    def __init__(self, value: _ReturnTypeVar) -> None:
        self.value = value


class _Raise:
    """Data type for indicating an exception should be raised."""

    def __init__(
        self,
        exception: BaseException,
        traceback: typing.Optional[types.TracebackType],
    ) -> None:
        self.exception = exception
        self.traceback = traceback


class _HandleCoroState(typing.Generic[_ReturnTypeVar]):  # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        *,
        coro: _TaskCoroType[_ReturnTypeVar],
        coro_input: typing.Any,
        respond_to_coro: _ResponderProtocol[_ReturnTypeVar],
    ) -> None:
        self.coro = coro
        self.coro_input = coro_input
        self.respond_to_coro = respond_to_coro


def _handle_async_tco_call(tco_call: 'TailCall[_ReturnTypeVar]') -> _HandleCoroState[_ReturnTypeVar]:
    async_func = typing.cast(rototiller.WrappableFuncType[typing.Any, typing.Any, _ReturnTypeVar], tco_call.func)
    return _HandleCoroState(
        coro=rototiller.Coro(async_func),
        coro_input=(tco_call.args, tco_call.kwargs),
        respond_to_coro=_coro_init,
    )


def _handle_sync_tco_call(tco_call: 'TailCall[_ReturnTypeVar]') -> _Return[_ReturnTypeVar]:
    sync_func = tco_call.func
    result = typing.cast(_ReturnTypeVar, sync_func(*tco_call.args, **tco_call.kwargs))
    action = _Return(result)
    return action


def _handle_exception(output: rototiller.Raised) -> _Raise:
    # XXX need to only clean up errors from user funcs, not from seedflow internals
    # clean up the traceback to be as readable as possible
    _, exception, traceback = output.value
    traceback = _strip_traceback(traceback)
    # we got here, there's an exception, but mypy complains it could be none
    exception = typing.cast(Exception, exception)
    action = _Raise(exception, traceback)
    return action


def _handle_tco_call(
    raised: rototiller.Raised,
    state: _HandleCoroState[_ReturnTypeVar],
) -> typing.Tuple[
    _HandleCoroState[_ReturnTypeVar],
    typing.Optional[_Return[_ReturnTypeVar]],
]:
    tco_call = typing.cast(TailCall[_ReturnTypeVar], raised.exc_value)
    if inspect.iscoroutinefunction(tco_call.func):
        state, action = _handle_async_tco_call(tco_call), None
    else:
        action = _handle_sync_tco_call(tco_call)
    return state, action


def _handle_task(
    task: _Task[_ReturnTypeVar],
    state: _HandleCoroState[_ReturnTypeVar],
) -> _HandleCoroState[_ReturnTypeVar]:
    try:
        if inspect.iscoroutinefunction(task.func):
            func = typing.cast(_TaskFuncType[_ReturnTypeVar], task.func)
            state.coro_input = run_tasks_from(func, *task.args, **task.kwargs)
        else:
            state.coro_input = task.func(*task.args, **task.kwargs)
    # necessarily broad exception
    except Exception:  # pylint: disable=broad-except
        # throw the exception back to the caller (the coro)
        state.coro_input = sys.exc_info()
        state.respond_to_coro = _coro_throw
    else:
        state.respond_to_coro = _coro_send
    return state


def _handle_unknown(
    output: rototiller.OutputType[_Task[typing.Any], _ReturnTypeVar],
    state: _HandleCoroState[_ReturnTypeVar],
) -> _HandleCoroState[_ReturnTypeVar]:  # pragma: no cover
    # this is here to alert the programmer of an error, but it's not really part
    # of the runtime behavior promised, so we're not testing it.
    state.coro_input = TypeError(
        f"Unrecognized output ({output}) - expected Returned, Raised, Yielded(_Task)",
    )
    state.respond_to_coro = _coro_throw
    return state


def _handle_coro_output(
    output: rototiller.OutputType[_Task[typing.Any], _ReturnTypeVar],
    state: _HandleCoroState[_ReturnTypeVar],
) -> typing.Tuple[
    _HandleCoroState[_ReturnTypeVar],
    typing.Union[_Return[_ReturnTypeVar], _Raise, None],
]:
    # XXX conflated: determining input type, deciding on response, responding
    action: typing.Union[_Return[_ReturnTypeVar], _Raise, None]
    if isinstance(output, rototiller.Returned):
        action = _Return(output.value)
    elif isinstance(output, rototiller.Raised) and isinstance(output.exc_value, TailCall):
        state, action = _handle_tco_call(output, state)
    elif isinstance(output, rototiller.Raised):
        action = _handle_exception(output)
    elif isinstance(output, rototiller.Yielded) and isinstance(output.value, _Task):
        state, action = _handle_task(output.value, state), None
    else:  # pragma: no cover
        # this is here to alert the programmer of an error, but it's not really part
        # of the runtime behavior promised, so we're not testing it.
        state, action = _handle_unknown(output, state), None
    return state, action


@types.coroutine
def _coro_helper(thing: _Task[_ReturnTypeVar]) -> typing.Generator[_Task[_ReturnTypeVar], _ReturnTypeVar, _ReturnTypeVar]:
    return (yield thing)


# [ API ]
# Exposing internals because mypy doesn't allow forward references of generic types.
TaskFuncType = _TaskFuncType[_ReturnTypeVar]
SyncFuncType = _SyncFuncType[_ReturnTypeVar]


@typing.overload
async def run(
    func: TaskFuncType[_ReturnTypeVar],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> _ReturnTypeVar:
    """Turn the given function and args into a task and yield it to the runner."""
    ...  # pragma: no coverage


@typing.overload  # noqa
async def run(
    func: SyncFuncType[_ReturnTypeVar],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> _ReturnTypeVar:
    """Turn the given function and args into a task and yield it to the runner."""
    ...  # pragma: no coverage


async def run(  # noqa
    func: typing.Union[TaskFuncType[_ReturnTypeVar], SyncFuncType[_ReturnTypeVar]],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> _ReturnTypeVar:
    """Turn the given function and args into a task and yield it to the runner."""
    # coro helper just yields the thing passed in back up
    # the caller will take it and run the func, then send the result back in
    # the coro helper will return that result.  That result has type _ReturnTypeVar,
    # therefor:
    result = await _coro_helper(_Task(func, *args, **kwargs))
    # This is necessary so that we can use typing.overload to properly define this function for
    # mypy, since the typing.overload and @types.coroutine don't seem to play nicely together
    return result


# pylint is wrong about typing.Generic
class TailCall(din.EqualityMixin, Exception, typing.Generic[_ReturnTypeVar]):  # pylint: disable=unsubscriptable-object
    """Tail Call Optimization helper class."""

    # pylint: disable-all
    @typing.overload
    def __init__(self, func: TaskFuncType[_ReturnTypeVar], *args: typing.Any, **kwargs: typing.Any) -> None:
        ...  # pragma: no cover

    @typing.overload  # noqa
    def __init__(self, func: SyncFuncType[_ReturnTypeVar], *args: typing.Any, **kwargs: typing.Any) -> None:
        ...  # pragma: no cover
    # pylint: enable-all

    def __init__(  # noqa
        self,
        func: typing.Union[SyncFuncType[_ReturnTypeVar], TaskFuncType[_ReturnTypeVar]],
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:  # pragma: no cover
        lines = [
            f"[seedflow.TailCall]",
            f"  func: {self.func.__module__}.{self.func.__qualname__}",
            f"  args:",
            *("\n".join(f"    {l}" for l in f"{a}".splitlines()) for a in self.args),
            f"  kwargs:",
            *("\n".join(f"    {l}" for l in f"{k}: {v}".splitlines()) for k, v in self.kwargs.items()),
        ]
        return "\n".join(lines)

    __repr__ = __str__


def run_tasks_from(
    func: TaskFuncType[_ReturnTypeVar],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> _ReturnTypeVar:
    """Run the tasks yielded by the given coroutine."""
    loop_state: _HandleCoroState[_ReturnTypeVar] = _HandleCoroState(
        coro=rototiller.Coro(func),
        coro_input=(args, kwargs),
        respond_to_coro=_coro_init,
    )
    action = None
    # XXX put while loop in own func?
    while True:
        output = loop_state.respond_to_coro(loop_state.coro, coro_input=loop_state.coro_input)
        loop_state, action = _handle_coro_output(output, state=loop_state)
        if isinstance(action, _Return):
            return action.value
        if isinstance(action, _Raise):
            raise action.exception.with_traceback(action.traceback)
        if action:  # pragma: no cover
            # this is here to alert the programmer of an error, but it's not really part
            # of the runtime behavior promised, so we're not testing it.
            raise RuntimeError(f"Unrecognized action returned by internal functions! {action}")


def as_sync(
    func: TaskFuncType[_ReturnTypeVar],
) -> SyncFuncType[_ReturnTypeVar]:
    """
    Decorate an awaitable such that it is run with seedflow when called.

    This makes a seedflow-awaitable function callable from a synchronous context.
    """
    @functools.wraps(func)
    def _wrapper(*args: typing.Any, **kwargs: typing.Any) -> _ReturnTypeVar:
        return run_tasks_from(func, *args, **kwargs)
    return _wrapper
