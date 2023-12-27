from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.measurement import measurement_router
from api.spirit import spirit_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(spirit_router.router)
app.include_router(measurement_router.router)
