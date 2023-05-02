"""
Foodindo App helps to automate lunch registration
and validation for Entri Office Lunch
"""

import pyqrcode
from os.path import exists
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import aioredis

app = FastAPI()

class Config():
    """
    The default redis URL
    """
    redis_url: str = 'redis://red-ch880ausi8uhth5le8c0:6379'

config = Config()
app = FastAPI(title='FastAPI Redis Tutorial')
redis = aioredis.from_url(config.redis_url, decode_responses=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
async def root() -> Response:
    """
    Index Page
    """
    user_ids: list = [1,2,3]
    removed: bool = bool(await redis.delete('test'))
    response: int = await redis.sadd('test', *user_ids)
    value: list = await redis.smembers('test')
    count: int = await redis.scard('test')
    return {
        "message": value,
        "count": count,
        "response": response,
        "is_removed": removed
    }

@app.get("/user/{user_id}/register")
async def register_user(user_id: str) -> Response:
    """
    Takes daily registrations from
    SlackBot integration
    """
    is_added: int = await redis.sadd('members', user_id)
    _: int = await redis.sadd('validator', user_id)
    qr_code_path: str = f"media/{user_id}.png"
    qr_code_file_path: str = f"http://foodindo.onrender.com/{qr_code_path}"
    if exists(qr_code_path):
        return {
        "data": f"{user_id} registered",
        "qr_code_url": qr_code_file_path
    }
    qr_code_url: str = f"https://foodindo.onrender.com/user/{user_id}/validate"
    qr_code: pyqrcode = pyqrcode.create(qr_code_url)
    qr_code.png(qr_code_path, scale = 6)
    if not is_added:
        return JSONResponse(
            content={
                "error": "User already registered",
                "qr_code_url": qr_code_file_path
            },
            status_code=400)
    return {
        "data": f"{user_id} registered",
        "qr_code_url": qr_code_file_path
    }


@app.get("/user/{user_id}/validate")
async def validate_user(user_id: str) -> Response:
    """
    Sample url with path
    """
    is_member: int = await redis.sismember('members', user_id)
    if not is_member:
        return JSONResponse(
            content={"error": "User not registered"},
            status_code=400)
    count: int = await redis.srem('validator', user_id)
    if not count:
        return JSONResponse(
            content={"error": "User already validated"},
            status_code=400)
    return {"data": "User Validated"}

@app.get("/total-registrations")
async def total_registrations() -> Response:
    """
    Returns the count of total user registrations
    for a day
    """
    total_count: int = await redis.scard('members')
    return {
        'total_count': total_count
    }
