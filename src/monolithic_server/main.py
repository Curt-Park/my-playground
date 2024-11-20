"""Simple monolithic server for N8N."""

import argparse
import logging
import time
from http import HTTPStatus
from typing import Callable

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from playwright.async_api import async_playwright
from youtube_transcript_api import YouTubeTranscriptApi

# Logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# API Server
app = FastAPI(title="N8N API Server")
logger.info("initialized fastapi")


# APIs
@app.get("/apis")
def apis(request: Request) -> list[str]:
    """Return all API end-points."""
    routes = {route.path for route in request.app.routes}
    routes -= {"/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect", "/apps"}
    return sorted(list(routes))


@app.get("/webpage")
async def webscraper(url: str) -> str:
    """Scrap the given web contents."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        await browser.close()
    return content


@app.get("/youtube-transcript")
def youtube_transcript(video_id: str) -> str:
    """Return youtube video script as a string."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=("en", "en-US", "ko"))
        transcript = " ".join([partial_transcript["text"].replace("\n", " ") for partial_transcript in transcript])
    except Exception as e:
        msg = str(e).replace("\n", " ")
        logger.info(msg)
        raise HTTPException(status_code=404, detail=msg) from e
    return transcript


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
    parser.add_argument("--port", type=int, default=9888, help="port number")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
