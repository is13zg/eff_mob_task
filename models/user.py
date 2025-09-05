from pydantic import BaseModel, Field, EmailStr

str20 = Field(..., max_length=20)


class UserRegister(BaseModel):
    name: str20
    last_name: str20
    father_name: str20
    email: EmailStr
    passwd: str = Field(...,min_length=6, max_length=30)
    rep_passwd: str = Field(...,min_length=6, max_length=30)





