from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from sqlalchemy.orm import Session
from utils.passwd import hash_password, verify_password