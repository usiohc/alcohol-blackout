from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import FieldValidationInfo


class Token(BaseModel):
    access_token: str
    token_type: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=20)
    passwordCheck: str = Field(min_length=8, max_length=20)

    @field_validator('username', 'email', 'password', 'passwordCheck')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise PydanticCustomError("ValueError",
                                      "빈 값은 허용되지 않습니다.",
                                      {"value": v})
            # raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'passwordCheck' in info.data and v != info.data['passwordCheck']:
            raise PydanticCustomError("ValueError",
                                      "비밀번호가 일치하지 않습니다.",
                                      {"value": v})
        return v


class UserLogin(BaseModel):
    pass
