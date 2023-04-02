import logging
import re
from typing import Optional, TypeVar
from fastapi import HTTPException
from pydantic import BaseModel, validator
from app.model.person import Sex


T = TypeVar('T')


# Get root logger
logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):

    username: str
    email: str
    name: str
    password: str
    phone_number: str
    birth: str
    sex: Sex
    profile: str = "base64"

    # Phone number validation
    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # Regex phone number
        regex = r"^[\+]?[0-9]{1,3}-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Invalid phone number"})
        return v

    # Sex validation
    @validator("sex")
    def sex_validation(cls, v):
        if hasattr(Sex, v) is False:
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Invalid sex"})
        return v


class LoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None
