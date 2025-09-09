from typing import Annotated

from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo

STR_20 = Annotated[str, Field(..., max_length=20)]
PASSWORD = Annotated[str, Field(..., min_length=6, max_length=30)]


class UserLogin(BaseModel):
    email: EmailStr
    passwd: PASSWORD

    @classmethod
    @field_validator("email")
    def lower_email(cls, v: str) -> str:
        return v.strip().lower()


class UserRegister(UserLogin):
    name: STR_20
    last_name: STR_20
    father_name: STR_20
    rep_passwd:  PASSWORD

    @classmethod
    @field_validator("rep_passwd")
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if "passwd" in info.data and v != info.data["passwd"]:
            raise ValueError("passwords do not match")
        return v


class UserOut(BaseModel):
    id: int
    name: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"