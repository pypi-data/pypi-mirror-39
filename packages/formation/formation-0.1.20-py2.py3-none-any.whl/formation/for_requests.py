import requests
from requests.compat import urljoin
from .formation import wrap, _REQ_HTTP, _RES_HTTP, _SESSION
from attr import attrib, attrs
import datetime

__all__ = ["build_sender", "build", "client"]


def client(cls=None):
    def client_decorator(cls):
        original_init = cls.__init__

        def now_iso(self):
            return datetime.datetime.utcnow().isoformat()

        def path(self, p):
            return requests.compat.urljoin(self.base_uri, p)

        def init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.request = build(
                middleware=kwargs.get("middleware", self.__class__.middleware)
            )
            self.base_uri = kwargs.get("base_uri", self.__class__.base_uri)

        cls.path = path
        cls.now_iso = now_iso
        cls.__init__ = init
        return cls

    if cls:
        return client_decorator(cls)
    return client_decorator


@attrs
class FormationHttpRequest(object):
    url = attrib()
    method = attrib(default="get")
    headers = attrib(default={})
    params = attrib(default={})
    auth = attrib(default=None)
    data = attrib(default=None)


def build_sender(middleware=[]):
    wrapped = wrap(requests_adapter, middleware=middleware)

    def sender(method, url, session_context={}, **kwargs):
        ctx = {
            _REQ_HTTP: FormationHttpRequest(url=url, method=method, **kwargs),
            _SESSION: session_context,
        }
        ctx = wrapped(ctx)
        return ctx[_RES_HTTP]

    return sender


def build(middleware=[], base_uri=None):
    class Sender(object):
        def __init__(self):
            self.base_uri = base_uri
            self.send = build_sender(middleware)

        def send(self, method, path, session_context={}, **kwargs):
            ctx = {
                _REQ_HTTP: FormationHttpRequest(
                    url=urljoin(self.base_uri, path), method=method, **kwargs
                ),
                _SESSION: session_context,
            }
            ctx = self.wrapped(ctx)
            return ctx[_RES_HTTP]

        def get(self, path, **kwargs):
            return self.send("get", path, **kwargs)

        def post(self, path, **kwargs):
            return self.send("post", path, **kwargs)

        def put(self, path, **kwargs):
            return self.send("put", path, **kwargs)

    return Sender


# TODO: pass more requests vars via req (e.g. timeout, retry)
def requests_adapter(ctx):
    req = ctx[_REQ_HTTP]
    meth = getattr(requests, req.method.lower())
    # TODO ship var as kwargs and not explicitly
    res = meth(
        req.url, headers=req.headers, params=req.params, auth=req.auth, data=req.data
    )
    ctx[_RES_HTTP] = res
    return ctx
