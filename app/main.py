from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.events import lifespan
from app.routers import (
    user_router,
    auth_router,
    role_router,
    permission_router
)
from app.conf import get_settings

origins = get_settings().origins

app = FastAPI(lifespan=lifespan)
app.title = "Barbershop"
app.description = "Barbershop API"
app.version = "0.0.1"
app.swagger_ui_parameters = {
    "filter": True
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(role_router)
router.include_router(permission_router)

app.include_router(router)

add_pagination(app)