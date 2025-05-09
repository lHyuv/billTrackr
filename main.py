from fastapi import FastAPI, HTTPException, Request, Depends, Body, status
from pydantic import BaseModel
from database import SessionLocal, engine
from models import billing_model, category_model, user_model

app = FastAPI()
@app.get('/', status_code = status.HTTP_200_OK)
async def home():
    return {"message": "Success"}