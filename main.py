from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates

from database import Base, engine
from models import user, category, sub_category, torrent
from routers import users, torrents, admin, categories, sub_categories

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.on_event("startup")
def startup_event():
    # Move the create_all call to the startup event
    Base.metadata.create_all(bind=engine, tables=[
        user.User.__table__,
        category.Category.__table__,
        sub_category.SubCategory.__table__,
        torrent.Torrent.__table__,
    ])


app.include_router(admin.router)
app.include_router(categories.router)
app.include_router(sub_categories.router)
app.include_router(torrents.router)
app.include_router(users.router)

from fastapi.responses import JSONResponse

@app.get("/manifest.json")
def manifest():
    return {
        "id": "org.zamunda.addon",
        "version": "1.0.0",
        "name": "Stremio Zamunda",
        "description": "Streams movies by scraping torrents from Zamunda.",
        "icon": "https://github.com/murrou-cell/zamunda-api/blob/main/logo/logo.jpg?raw=true",
        "resources": ["stream"],
        "types": ["movie", "series"],
        "idPrefixes": ["tt"],
        "catalogs": [],
        "behaviorHints": {
            "configurable": True,
            "configurationRequired": True
        }
    }

@app.get("/stream/{type}/{id}")
def stream(type: str, id: str):
    # Временно за тест
    if id == "tt1375666":
        return JSONResponse([
            {
                "title": "Inception 1080p",
                "infoHash": "d2474e86c95b19b8bcfdb92bc12c9d44667cfa36",
                "fileIdx": 0
            }
        ])
    return JSONResponse([])


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
