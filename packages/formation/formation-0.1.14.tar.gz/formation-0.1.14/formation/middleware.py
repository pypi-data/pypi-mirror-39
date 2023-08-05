import threading
import datetime
from uuid import uuid4
from toolz.curried import valfilter
import os


def create_request_id(key="x-request-id", idgen=uuid4):
    def requests_id(ctx, next):
        headers = ctx["fmtn.req"].headers
        headers[key] = headers.get(key, str(idgen()))
        ctx["req.id"] = headers[key]
        ctx = next(ctx)
        return ctx

    return requests_id


def create_request_duration(now=datetime.datetime.now):
    def request_duration(ctx, next):
        start = now()
        ctx = next(ctx)
        end = now() - start
        ctx["req.duration_us"] = end.microseconds
        return ctx

    return request_duration


def logger_context(
    request_id=None,
    request_parent_id=None,
    namespace="service",
    env="local",
    sha="dev",
    version="0.0.1",
    scope="service",
    uid=None,
):
    pid = os.getpid()
    tid = threading.get_ident()
    return {
        "v": version,
        "sha": sha,
        "env": env,
        "pid": pid,
        "tid": tid,
        "uid": uid,
        "scope": scope,
        "ns": namespace,
        "rid": request_id,
        "rid_p": request_parent_id,
    }


def create_request_logger(
    logger,
    context_fn=logger_context,
    namespace="service",
    scope="all",
    env="local",
    sha="dev",
    version="0.01",
):
    no_nones = valfilter(lambda x: x)

    def request_logger(ctx, next):
        req = ctx["fmtn.req"]
        request_id = ctx["req.id"]
        uid = ctx.get("user.id", None)
        request_parent_id = ctx.get("req.parent.id", None)
        msg = "request.http"

        log = logger.bind(
            **context_fn(
                env=env,
                sha=sha,
                version=version,
                request_id=request_id,
                request_parent_id=request_parent_id,
                scope=scope,
                uid=uid,
            )
        )
        log.info(msg, url=req.url, method=req.method, params=no_nones(req.params))
        log.debug(msg, headers=req.headers)

        ctx = next(ctx)

        res = ctx["fmtn.res"]

        msg = "response.http"
        log.info(
            msg,
            url=res.request.url,
            status=res.status_code,
            method=res.request.method,
            elapsed=res.elapsed,
            size=len(res.content),
            duration_us=ctx.get("req.duration_us", None),
        )
        log.debug(msg, headers=res.headers)
        return ctx

    return request_logger


def retry(max_retries=3):
    def retry_middleware(ctx, call):
        try:
            res = call(ctx)
            return res
        except Exception as ex:
            retries = ctx.get("fmtn.retry", 0)
            if retries > max_retries:
                raise ex
            ctx["fmtn.retry"] = 1 + retries
            # TODO exponential backoff
            res = retry_middleware(ctx, call)
            return res

    return retry_middleware
