from collections import defaultdict
from functools import wraps
from typing import Callable, Union, Dict, Coroutine

from .compat import call_async, asynccontextmanager
from .request import Request
from .response import Response
from .routing import Route

HookFunction = Callable[[Request, Response, dict], Coroutine]
HookCollection = Dict[Route, HookFunction]

BEFORE = 'before'
AFTER = 'after'


async def empty_hook(req: Request, res: Response, params: dict):
    pass


class Hooks:
    """Collection of hooks."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hooks: Dict[str, HookCollection] = {
            BEFORE: defaultdict(lambda: empty_hook),
            AFTER: defaultdict(lambda: empty_hook),
        }

    def before(self, hook_function: HookFunction, *args, **kwargs):
        return self._hook_decorator(BEFORE, hook_function, *args, **kwargs)

    def after(self, hook_function: HookFunction, *args, **kwargs):
        return self._hook_decorator(AFTER, hook_function, *args, **kwargs)

    def _hook_decorator(
        self, hook: str, hook_function: HookFunction, *args, **kwargs
    ):
        def decorator(hookable: Union[Route, Callable]):
            """Bind the hook function to the given hookable object.

            Support for decorating a route or a class method enables
            using hooks in the following contexts:
            - On a function-based view (before @api.route()).
            - On top of a class-based view (before @api.route()).
            - On a class-based view method.

            Parameters
            ----------
            hookable : Route or (unbound) class method
            """
            nonlocal hook_function
            full_hook_function = hook_function

            async def hook_function(req: Request, res: Response, params: dict):
                await call_async(
                    full_hook_function, req, res, params, *args, **kwargs
                )

            if isinstance(hookable, Route):
                route = hookable
                self._hooks[hook][route] = hook_function
                return route
            else:
                view: Callable = hookable

                @wraps(view)
                async def with_hook(self, req, res, **kw):
                    if hook == BEFORE:
                        await hook_function(req, res, kw)
                    await call_async(view, self, req, res, **kw)
                    if hook == AFTER:
                        await hook_function(req, res, kw)

                return with_hook

        return decorator

    @asynccontextmanager
    async def on(self, route, request, response, params):
        """Execute `before` hooks on enter and `after` hooks on exit."""
        await call_async(self._hooks[BEFORE][route], request, response, params)
        yield
        await call_async(self._hooks[AFTER][route], request, response, params)


# Default hooks collection
_hooks = Hooks()


class HooksMixin:
    """Mixin that provides hooks to application classes."""

    def get_hooks(self):
        return _hooks

    def before(self, hook_function: HookFunction, *args, **kwargs):
        """Register a before hook on a route.

        ::: tip NOTE
        `@api.before()` should be placed  **above** `@api.route()`
        when decorating a view.
        :::

        # Parameters
        hook_function (callable):\
            A synchronous or asynchronous function with the signature:
            `(req, res, params) -> None`.
        """
        return self.get_hooks().before(hook_function, *args, **kwargs)

    def after(self, hook_function: HookFunction, *args, **kwargs):
        """Register an after hook on a route.

        ::: tip NOTE
        `@api.after()` should be placed **above** `@api.route()`
        when decorating a view.
        :::

        # Parameters
        hook_function (callable):\
            A synchronous or asynchronous function with the signature:
            `(req, res, params) -> None`.
        """
        return self.get_hooks().after(hook_function, *args, **kwargs)
