from fastapi import FastAPI, Body, status
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from typing import List
from project.config import CONFIG

app = FastAPI()


class CommentBase(BaseModel):
    body: str


class Comment(Document, CommentBase):
    pass


@app.on_event("startup")
async def start():
    # init db
    client = AsyncIOMotorClient(CONFIG.MONGODB_CONNSTRING)
    await init_beanie(database=client[CONFIG.DB_NAME], document_models=[Comment])


@app.get("/")
async def hello():
    return {"hello": "world"}


@app.get("/comments", response_model=List[Comment])
async def list_comments():
    comments = Comment.all()
    return await comments.to_list()


@app.post("/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(body: CommentBase = Body(...)):
    return await Comment(**body.dict()).create()
