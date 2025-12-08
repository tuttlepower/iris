import ipaddress
import logging
from typing import Optional
from urllib.parse import unquote, urlparse, urlunparse

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("iris")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

READER_PREFIX = "https://r.jina.ai/"
ARCHIVE_PREFIX = "https://archive.ph/"
WAYBACK_PREFIX = "https://web.archive.org/"
TWELVE_FT_PREFIX = "https://12ft.io/"

RAW_TIMEOUT = httpx.Timeout(10.0, connect=5.0)
MAX_RAW_BYTES = 1_000_000  # 1MB limit for raw responses


class BlockedAddress(HTTPException):
    def __init__(self, detail: str = "Blocked host"):
        super().__init__(status_code=403, detail=detail)


def normalize_target(raw_url: str) -> str:
    if not raw_url:
        raise HTTPException(status_code=400, detail="Invalid URL")

    decoded = unquote(raw_url).strip()
    if not decoded:
        raise HTTPException(status_code=400, detail="Invalid URL")

    parsed = urlparse(decoded)
    if not parsed.scheme:
        parsed = urlparse(f"https://{decoded}")

    if parsed.scheme not in {"http", "https"}:
        raise HTTPException(status_code=400, detail="Invalid URL scheme")

    host = parsed.hostname
    if not host:
        raise HTTPException(status_code=400, detail="Invalid URL")

    host_lower = host.lower()
    if host_lower == "localhost" or host_lower.startswith("localhost"):
        raise BlockedAddress("Localhost is not allowed")

    try:
        ip = ipaddress.ip_address(host)
        if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_unspecified:
            raise BlockedAddress("Private addresses are not allowed")
    except ValueError:
        # Host is not a direct IP address
        if host_lower.startswith("127."):
            raise BlockedAddress("Loopback addresses are not allowed")

    sanitized = parsed._replace(fragment="")
    return urlunparse(sanitized)


def log_request(request: Request, target: Optional[str]) -> None:
    logger.info("%s %s -> %s", request.method, request.url.path, target or "-")
    request.state.logged = True


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/a/{url:path}")
async def archive_redirect(url: str, request: Request) -> RedirectResponse:
    target = normalize_target(url)
    log_request(request, target)
    return RedirectResponse(url=f"{ARCHIVE_PREFIX}{target}", status_code=302)


@app.get("/w/{url:path}")
async def wayback_redirect(url: str, request: Request) -> RedirectResponse:
    target = normalize_target(url)
    log_request(request, target)
    return RedirectResponse(url=f"{WAYBACK_PREFIX}{target}", status_code=302)


@app.get("/12/{url:path}")
async def twelve_ft_redirect(url: str, request: Request) -> RedirectResponse:
    target = normalize_target(url)
    log_request(request, target)
    return RedirectResponse(url=f"{TWELVE_FT_PREFIX}{target}", status_code=302)


@app.get("/r/{url:path}")
async def reader_redirect(url: str, request: Request) -> RedirectResponse:
    target = normalize_target(url)
    log_request(request, target)
    return RedirectResponse(url=f"{READER_PREFIX}{target}", status_code=302)


@app.get("/raw/{url:path}")
async def raw_content(url: str, request: Request) -> Response:
    target = normalize_target(url)
    log_request(request, target)

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=RAW_TIMEOUT) as client:
            async with client.stream("GET", target, headers={"User-Agent": "iris/fastapi"}) as resp:
                body = bytearray()
                async for chunk in resp.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_RAW_BYTES:
                        raise HTTPException(status_code=400, detail="Response too large")

                content_type = resp.headers.get("content-type", "text/html")
                return Response(content=bytes(body), media_type=content_type, status_code=resp.status_code)
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Upstream fetch timed out") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=504, detail="Upstream fetch failed") from exc


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    if not getattr(request.state, "logged", False):
        target = None
        if request.path_params:
            target = request.path_params.get("url")
        log_request(request, target)
    if status_code in {400, 403, 404, 504}:
        context = {
            "request": request,
            "status_code": status_code,
            "detail": exc.detail or "Unexpected error",
        }
        return templates.TemplateResponse("error.html", context, status_code=status_code)
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": status_code, "detail": exc.detail},
        status_code=status_code,
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if not getattr(request.state, "logged", False):
        target = None
        if request.path_params:
            target = request.path_params.get("url")
        log_request(request, target)
    context = {"request": request, "status_code": 404, "detail": "Page not found"}
    return templates.TemplateResponse("error.html", context, status_code=404)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if not getattr(request.state, "logged", False):
        target = None
        if request.path_params:
            target = request.path_params.get("url")
        log_request(request, target)
    logger.exception("Unhandled error: %s", exc)
    context = {"request": request, "status_code": 500, "detail": "Internal server error"}
    return templates.TemplateResponse("error.html", context, status_code=500)
