
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import LOCAL_ORIGINS, DEBUG

from api.cocktail import cocktail_router
from api.spirit import spirit_router
from api.material import material_router
from api.user import user_router
from api.bookmark import bookmark_router
from api.user.email import email


app = FastAPI()

origins = [
    # for local development -> frontend (Vite)

]

if DEBUG:
    origins += ["*"] 
elif LOCAL_ORIGINS:
    origins += LOCAL_ORIGINS

# middleware 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# router 등록
app.include_router(spirit_router.router)
app.include_router(material_router.router)
app.include_router(cocktail_router.router)
app.include_router(user_router.router)
app.include_router(bookmark_router.router)
app.include_router(email.router)


# swagger 설정
app.title = "ACBO API"
app.description = "ACBO API 문서입니다."
app.version = "0.0.1"
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"
app.redoc_url = "/redoc"
