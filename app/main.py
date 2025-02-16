from fastapi import FastAPI, Depends
from app.routers import routes, secure
from app.models import models
from app.database.database import engine
from app.security.auth import get_user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    routes.router,
    prefix="/api/v1/public"
)

app.include_router(
    secure.router,
    prefix="/api/v1/pubsecurelic",
    dependencies=[Depends(get_user)]
)
