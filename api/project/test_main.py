from traceback import print_exc
import pytest
import asyncio
from decouple import config
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from fastapi import status

from project.main import app as app
from project.main import Comment
from project.config import CONFIG
from beanie import init_beanie

# Override config settings before loading the app
CONFIG.TESTING = True
CONFIG.MONGODB_CONNSTRING = config(
    "TEST_MONGO_URI", default="mongodb://admin:password@mongodb"
)
CONFIG.DB_NAME = "smapi_test"


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


async def startup():
    """Initializes test database"""

    print("\nStarting Test Suite")
    print(f"Creating database '{CONFIG.DB_NAME}'")
    app.client = AsyncIOMotorClient(CONFIG.MONGODB_CONNSTRING)
    # https://roman-right.github.io/beanie/tutorial/initialization/
    await init_beanie(
        app.client[CONFIG.DB_NAME],
        document_models=[Comment],
    )


async def shutdown():
    """Empties the test database"""
    print("\nShutting Down")
    await app.client.drop_database(CONFIG.DB_NAME)
    print(f"Database '{CONFIG.DB_NAME}' dropped")


@pytest.fixture(scope="session", autouse=True)
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        try:
            await startup()
        except:
            print_exc()
        finally:
            yield client
            await shutdown()


async def test_hello_world(client):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["hello"] == "world"


async def test_comments(client):
    COMMENT_BODY = "comment"

    async def _create_comment():
        response = await client.post("/comments", json={"body": COMMENT_BODY})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["body"] == COMMENT_BODY

    async def _list_comments():
        response = await client.get("/comments")

        assert response.status_code == status.HTTP_200_OK
        comments = response.json()
        assert len(comments) == 1
        assert comments[0]["body"] == COMMENT_BODY

    await _create_comment()
    await _list_comments()
