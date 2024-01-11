from fastapi import FastAPI
from core.config import local_origin
from starlette.middleware.cors import CORSMiddleware

from api.cocktail import cocktail_router
from api.spirit import spirit_router
from api.material import material_router
from api.user import user_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

if local_origin:
    origins += local_origin
else:
    print(local_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(spirit_router.router)
app.include_router(material_router.router)
app.include_router(cocktail_router.router)
app.include_router(user_router.router)
