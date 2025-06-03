from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.events.lifespan import lifespan
from app.config import get_settings

app = FastAPI(lifespan=lifespan)
app.title = "Barbershop"
app.description = "Barbershop API"
app.version = "0.0.1"
app.swagger_ui_parameters = {
    "filter": True
}

print(get_settings().db_url)

add_pagination(app)

