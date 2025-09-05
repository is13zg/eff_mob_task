from typing import Annotated

from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo

STR_20 = Annotated[str, Field(..., max_length=20)]
PASSWORD = Annotated[str, Field(..., min_length=6, max_length=30)]


class UserRegister(BaseModel):
    name: STR_20
    last_name: STR_20
    father_name: STR_20
    email: EmailStr
    passwd: str = PASSWORD
    rep_passwd: str = PASSWORD

    @field_validator("rep_passwd")
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if "passwd" in info.data and v != info.data["passwd"]:
            raise ValueError("passwords do not match")
        return v


class UserOut(BaseModel):
    id: int
    name: str
