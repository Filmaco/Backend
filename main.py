from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuario_router import router as usuario_router
from routes.video_router import router as video_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(video_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


