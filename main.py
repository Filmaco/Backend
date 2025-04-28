from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usuario_router import router as usuario_router
from routes.auth_router import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(auth_router)
