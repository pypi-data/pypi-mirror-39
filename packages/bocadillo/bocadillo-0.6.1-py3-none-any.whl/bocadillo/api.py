"""The Bocadillo API class."""
import os
from typing import Optional, Tuple, Type, List, Dict, Any, Union, Callable

from asgiref.wsgi import WsgiToAsgi
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.testclient import TestClient
from uvicorn.main import run, get_logger
from uvicorn.reloaders.statreload import StatReload

from .compat import call_all_async
from .cors import DEFAULT_CORS_CONFIG
from .error_handlers import ErrorHandler, handle_http_error
from .exceptions import HTTPError
from .hooks import HooksMixin
from .media import Media
from .meta import APIMeta
from .middleware import CommonMiddleware, RoutingMiddleware
from .redirection import Redirection
from .request import Request
from .response import Response
from .routing import RoutingMixin
from .static import static
from .templates import TemplatesMixin
from .types import ASGIApp, WSGIApp, ASGIAppInstance


class API(TemplatesMixin, RoutingMixin, HooksMixin, metaclass=APIMeta):
    """The all-mighty API class.

    This class implements the [ASGI](https://asgi.readthedocs.io) protocol.

    # Example

    ```python
    >>> import bocadillo
    >>> api = bocadillo.API()
    ```

    # Parameters

    templates_dir (str):
        The name of the directory where templates are searched for,
        relative to the application entry point.
        Defaults to `'templates'`.
    static_dir (str):
        The name of the directory containing static files, relative to
        the application entry point. Set to `None` to not serve any static
        files.
        Defaults to `'static'`.
    static_root (str):
        The path prefix for static assets.
        Defaults to `'static'`.
    allowed_hosts (list of str, optional):
        A list of hosts which the server is allowed to run at.
        If the list contains `'*'`, any host is allowed.
        Defaults to `['*']`.
    enable_cors (bool):
        If `True`, Cross Origin Resource Sharing will be configured according
        to `cors_config`. Defaults to `False`.
        See also [CORS](../topics/features/cors.md).
    cors_config (dict):
        A dictionary of CORS configuration parameters.
        Defaults to `dict(allow_origins=[], allow_methods=['GET'])`.
    enable_hsts (bool):
        If `True`, enable HSTS (HTTP Strict Transport Security) and automatically
        redirect HTTP traffic to HTTPS.
        Defaults to `False`.
        See also [HSTS](../topics/features/hsts.md).
    media_type (str):
        Determines how values given to `res.media` are serialized.
        Can be one of the supported media types.
        Defaults to `'application/json'`.
        See also [Media](../topics/request-handling/media.md).
    """

    _error_handlers: List[Tuple[Type[Exception], ErrorHandler]]

    def __init__(
        self,
        templates_dir: str = 'templates',
        static_dir: Optional[str] = 'static',
        static_root: Optional[str] = 'static',
        allowed_hosts: List[str] = None,
        enable_cors: bool = False,
        cors_config: dict = None,
        enable_hsts: bool = False,
        media_type: Optional[str] = Media.JSON,
    ):
        super().__init__(templates_dir=templates_dir)

        self._error_handlers = []
        self.add_error_handler(HTTPError, handle_http_error)

        self._extra_apps: Dict[str, Any] = {}

        self.client = self._build_client()

        if static_dir is not None:
            if static_root is None:
                static_root = static_dir
            self.mount(static_root, static(static_dir))

        if allowed_hosts is None:
            allowed_hosts = ['*']
        self.allowed_hosts = allowed_hosts

        if cors_config is None:
            cors_config = {}
        self.cors_config = {**DEFAULT_CORS_CONFIG, **cors_config}

        self._media = Media(media_type=media_type)

        # Middleware
        self._routing_middleware = RoutingMiddleware(self)
        self._common_middleware = CommonMiddleware(self._routing_middleware)
        self.add_middleware(
            TrustedHostMiddleware, allowed_hosts=self.allowed_hosts
        )
        if enable_cors:
            self.add_middleware(CORSMiddleware, **self.cors_config)
        if enable_hsts:
            self.add_middleware(HTTPSRedirectMiddleware)

    def get_template_globals(self):
        return {'url_for': self.url_for}

    def _build_client(self) -> TestClient:
        return TestClient(self)

    def mount(self, prefix: str, app: Union[ASGIApp, WSGIApp]):
        """Mount another WSGI or ASGI app at the given prefix.

        # Parameters
        prefix (str): A path prefix where the app should be mounted, e.g. `'/myapp'`.
        app: An object implementing [WSGI](https://wsgi.readthedocs.io) or [ASGI](https://asgi.readthedocs.io) protocol.
        """
        if not prefix.startswith('/'):
            prefix = '/' + prefix
        self._extra_apps[prefix] = app

    @property
    def media_type(self) -> str:
        """The currently configured media type.

        When setting it to a value outside of built-in or custom media types,
        an `UnsupportedMediaType` exception is raised.
        """
        return self._media.type

    @media_type.setter
    def media_type(self, media_type: str):
        self._media.type = media_type

    @property
    def media_handlers(self) -> dict:
        """The dictionary of supported media handlers.

        You can access, edit or replace this at will.
        """
        return self._media.handlers

    @media_handlers.setter
    def media_handlers(self, media_handlers: dict):
        self._media.handlers = media_handlers

    def add_error_handler(
        self, exception_cls: Type[Exception], handler: ErrorHandler
    ):
        """Register a new error handler.

        # Parameters
        exception_cls (Exception class):
            The type of exception that should be handled.
        handler (callable):
            The actual error handler, which is called when an instance of
            `exception_cls` is caught.
            Should accept a `req`, a `res` and an `exc`.
        """
        self._error_handlers.insert(0, (exception_cls, handler))

    def error_handler(self, exception_cls: Type[Exception]):
        """Register a new error handler (decorator syntax).

        # Example
        ```python
        >>> import bocadillo
        >>> api = bocadillo.API()
        >>> @api.error_handler(KeyError)
        ... def on_key_error(req, res, exc):
        ...     pass  # perhaps set res.content and res.status_code
        ```
        """

        def wrapper(handler):
            self.add_error_handler(exception_cls, handler)
            return handler

        return wrapper

    def _find_handlers(self, exception):
        return (
            handler
            for err_type, handler in self._error_handlers
            if isinstance(exception, err_type)
        )

    def _handle_exception(self, request, response, exception) -> None:
        """Handle an exception raised during dispatch.

        At most one handler is called for the exception: the first one
        to support it.

        If no handler was registered for the exception, it is raised.
        """
        for handler in self._find_handlers(exception):
            handler(request, response, exception)
            break
        else:
            raise exception from None

    def redirect(
        self,
        *,
        name: str = None,
        url: str = None,
        permanent: bool = False,
        **kwargs
    ):
        """Redirect to another route.

        # Parameters
        name (str): name of the route to redirect to.
        url (str): URL of the route to redirect to, required if `name` is ommitted.
        permanent (bool):
            If `False` (the default), returns a temporary redirection (302).
            If `True`, returns a permanent redirection (301).
        kwargs (dict):
            Route parameters.

        # Raises
        Redirection: an exception that will be caught by #API.dispatch().
        """
        if name is not None:
            url = self.url_for(name=name, **kwargs)
        else:
            assert url is not None, 'url is expected if no route name is given'
        raise Redirection(url=url, permanent=permanent)

    def _is_routing_middleware(self, middleware_cls) -> bool:
        return hasattr(middleware_cls, 'dispatch')

    def add_middleware(self, middleware_cls, **kwargs):
        """Register a middleware class.

        See also [Middleware](../topics/features/middleware.md).

        # Parameters

        middleware_cls (Middleware class):
            It should be a #~some.middleware.RoutingMiddleware class (not an instance!), or any
            concrete subclass or #~some.middleware.Middleware.
        """
        if self._is_routing_middleware(middleware_cls):
            self._routing_middleware.add(middleware_cls, **kwargs)
        else:
            self._common_middleware.add(middleware_cls, **kwargs)

    async def dispatch(
        self,
        request: Request,
        before: List[Callable] = None,
        after: List[Callable] = None,
    ) -> Response:
        """Dispatch a request and return a response.

        For the exact algorithm, see
        [How are requests processed?](../topics/request-handling/routes-url-design.md#how-are-requests-processed).

        # Parameters
        request (Request): an inbound HTTP request.
        before (list of callables): a list of middleware `before_dispatch` hooks.
        after (list of callables): a list of middleware `after_dispatch` hooks.

        # Returns
        response (Response): an HTTP response.
        """
        if before is None:
            before = []
        if after is None:
            after = []

        response = Response(request, media=self._media)

        try:
            match = self._router.match(request.url.path)
            if match is None:
                raise HTTPError(status=404)

            route, params = match.route, match.params
            route.raise_for_method(request)

            try:
                await call_all_async(before, request)
                hooks = self.get_hooks().on(route, request, response, params)
                async with hooks:
                    await route(request, response, **params)
                await call_all_async(after, request, response)
            except Redirection as redirection:
                response = redirection.response

        except Exception as e:
            self._handle_exception(request, response, e)

        return response

    def find_app(self, scope: dict) -> ASGIAppInstance:
        """Return the ASGI application suited to the given ASGI scope.

        This is also what `API.__call__(self)` returns.

        # Parameters
        scope (dict):
            An ASGI scope.

        # Returns
        app:
            An ASGI application instance
            (either `self` or an instance of a sub-app).
        """
        path: str = scope['path']

        # Return a sub-mounted extra app, if found
        for prefix, app in self._extra_apps.items():
            if not path.startswith(prefix):
                continue
            # Remove prefix from path so that the request is made according
            # to the mounted app's point of view.
            scope['path'] = path[len(prefix) :]
            try:
                return app(scope)
            except TypeError:
                app = WsgiToAsgi(app)
                return app(scope)

        return self._common_middleware(scope)

    def run(
        self,
        host: str = None,
        port: int = None,
        debug: bool = False,
        log_level: str = 'info',
    ):
        """Serve the application using [uvicorn](https://www.uvicorn.org).

        For further details, refer to
        [uvicorn settings](https://www.uvicorn.org/settings/).

        # Parameters

        host (str):
            The host to bind to.
            Defaults to `'127.0.0.1'` (localhost).
            If not given and `$PORT` is set, `'0.0.0.0'` will be used to
            serve to all known hosts.
        port (int):
            The port to bind to.
            Defaults to `8000` or (if set) the value of the `$PORT` environment
            variable.
        debug (bool):
            Whether to serve the application in debug mode. Defaults to `False`.
        log_level (str):
            A logging level for the debug logger. Must be a logging level
            from the `logging` module. Defaults to `'info'`.
        """
        if 'PORT' in os.environ:
            port = int(os.environ['PORT'])
            if host is None:
                host = '0.0.0.0'

        if host is None:
            host = '127.0.0.1'

        if port is None:
            port = 8000

        if debug:
            reloader = StatReload(get_logger(log_level))
            reloader.run(
                run,
                {
                    'app': self,
                    'host': host,
                    'port': port,
                    'log_level': log_level,
                    'debug': debug,
                },
            )
        else:
            run(self, host=host, port=port)

    def __call__(self, scope: dict) -> ASGIAppInstance:
        return self.find_app(scope)
