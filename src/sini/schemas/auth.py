from pydantic import BaseModel, Field


class OtpRequest(BaseModel):
    phone_number: str


class OtpVerify(BaseModel):
    phone_number: str
    code: str = Field(min_length=6, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
