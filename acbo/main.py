import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from api.bookmark import bookmark_router
from api.cocktail import cocktail_router
from api.material import material_router
from api.spirit import spirit_router
from api.user import user_router
from api.user.email import email
from core.config import DEBUG, LOCAL_ORIGINS, SWAGGER_PASSWORD, SWAGGER_USER

app = FastAPI(docs_url=None, redoc_url=None)

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
app.description = "Alcohol Blackout API 문서입니다."
app.version = "0.0.2"
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"
app.redoc_url = "/redoc"

# docs, openapi 셀프 호스팅
security = HTTPBasic()


def get_admin(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), SWAGGER_USER.encode("utf8")
    )
    correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), SWAGGER_PASSWORD.encode("utf8")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return "None"


@app.get("/docs", include_in_schema=False)
async def get_docs(_: Annotated[str, Depends(get_admin)]):
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title=app.title + " - Swagger UI"
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi(_: Annotated[str, Depends(get_admin)]):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
