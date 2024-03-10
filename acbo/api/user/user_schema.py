from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


class Token(BaseModel):
    access_token: str
    token_type: str
    email: EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    email: EmailStr = Field(max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)
    passwordCheck: str = Field(min_length=8, max_length=20)

    @field_validator("passwordCheck")
    def passwords_match(cls, v, info: FieldValidationInfo):
        if v != info.data["password"]:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v


class UserLogin(Token):
    username: str


class UserUpdateUsername(BaseModel):
    username: str = Field(min_length=2, max_length=15)


class UserUpdatePassword(BaseModel):
    password: str = Field(min_length=8, max_length=20)
    passwordCheck: str = Field(min_length=8, max_length=20)

    @field_validator("passwordCheck")
    def passwords_match(cls, v, info: FieldValidationInfo):
        if v != info.data["password"]:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v
