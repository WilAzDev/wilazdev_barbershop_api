from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.events import lifespan
from app.conf import get_settings
from app.routers import (
    user_router
)

app = FastAPI(lifespan=lifespan)
app.title = "Barbershop"
app.description = "Barbershop API"
app.version = "0.0.1"
app.swagger_ui_parameters = {
    "filter": True
}

app.include_router(user_router)

add_pagination(app)

