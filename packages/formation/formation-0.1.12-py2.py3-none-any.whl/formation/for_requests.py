import requests
from .formation import wrap
from attr import attrib, attrs, fields, asdict

__all__ = ["build_sender"]


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

    def sender(method, url, **kwargs):
        ctx = {"req": FormationHttpRequest(url=url, method=method, **kwargs)}
        ctx = wrapped(ctx)
        return ctx["res"]

    return sender


def requests_adapter(ctx):
    req = ctx["req"]
    meth = getattr(requests, req.method.lower())
    # TODO ship var as kwargs and not explicitly
    res = meth(
        req.url, headers=req.headers, params=req.params, auth=req.auth, data=req.data
    )
    ctx["res"] = res
    return ctx
