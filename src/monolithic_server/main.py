"""Simple monolithic server for N8N."""
import argparse
import datetime
import os
import time
import logging
from http import HTTPStatus
from typing import Callable

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response

from requests_html import HTMLSession
from bs4 import BeautifulSoup

logger = logging.getLogger()


# API Server
app = FastAPI(title="N8N API Server")
logger.debug("fastapi app initialized")


# APIs
@app.get("/apis")
def apis(request: Request) -> list[str]:
    """Return all API end-points."""
    routes = {route.path for route in request.app.routes}
    routes -= {"/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect", "/apps"}
    return sorted(list(routes))


@app.get("/webpage")
def webscraper(url: str):
    """"""
    session = HTMLSession()
    response = session.get(url)

    response.html.render()

    soup = BeautifulSoup(response.html.html, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    return rows


# Middlewares
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable[[Request], Response]) -> Response:
    """API processing time measurement."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    method, path = request.scope["method"], request.scope["root_path"] + request.scope["path"]
    logger.info(
        "%s:%s processed in %f s [status code: %d %s]",
        method,
        path,
        process_time,
        response.status_code,
        HTTPStatus(response.status_code).phrase,
    )
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0", help="host ip")
    parser.add_argument("--port", type=int, default=9100, help="port number")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, access_log=False)
