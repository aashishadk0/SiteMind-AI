from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database.init_db import initialize_database
from backend.app.routers import (
    auth,
    chat,
    scraper,
    ai,
    health
)
from backend.app.routers import knowledge
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="SiteMind AI",
    version="1.0.0"
)

# Project directories
BASE_DIR = Path(__file__).resolve().parent

# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

# Static files (CSS, JS, Images)
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)

app.include_router(auth.router)

app.include_router(chat.router)

app.include_router(scraper.router)

app.include_router(ai.router)

app.include_router(knowledge.router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )