from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.controllers import auth, post
from src.database import database, metadata, engine
from src.exceptions import NotFoundPostError


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.post import posts
    
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(post.router)


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )