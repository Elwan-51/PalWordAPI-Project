from fastapi import FastAPI, Depends, HTTPException, status
from app.internal import loader
import json
from typing import Annotated
app = FastAPI()

with open("app/config.json", "r") as files:
    config = json.load(files)
    loader.load_plugins(config["routers"], app)


@app.get("/")
async def root():
    return {"message": "Hello World"}

