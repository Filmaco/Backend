from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuario_router import router as usuario_router
from routes.video_router import router as video_router
from routes.playlist_router import router as playlist_router
from routes.comentario_router import router as comentario_router
from routes.seguir_usuarios_router import router as seguir_router
from routes.avaliacao_router import router as avaliacao_router
from routes.estatisticas_router import router as estatisticas_router
from routes.avaliacao_router import router as avaliacao_router
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
app.include_router(playlist_router)
app.include_router(comentario_router)
app.include_router(seguir_router)
app.include_router(avaliacao_router)
app.include_router(estatisticas_router)
app.include_router(avaliacao_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


