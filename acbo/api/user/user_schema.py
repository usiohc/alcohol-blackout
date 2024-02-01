from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import FieldValidationInfo


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

class Token(BaseModel):
    access_token: str
    token_type: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=20)
    passwordCheck: str = Field(min_length=8, max_length=20)

    # @field_validator('username', 'email', 'password'')
    # def not_empty(cls, v):
    #     if not v or not v.strip():
    #         raise PydanticCustomError("ValueError",
    #                                   "빈 값은 허용되지 않습니다.",
    #                                   {"value": v})
    #     return v

    @field_validator('passwordCheck')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if v != info.data['password']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v


class UserLogin(BaseModel):
    pass


class UserVerification(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    email: EmailStr = Field(max_length=100)
