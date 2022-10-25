from typing import Optional

from pydantic import BaseModel


class UpdateStreamer(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    user_login: Optional[str] = None
    user_name: Optional[str] = None
    game_id: Optional[int] = None
    game_name: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    viewer_count: Optional[int] = None
    started_at: Optional[str] = None
    language: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tag_ids: Optional[list] = None
    is_mature: Optional[bool] = None


class Streamer(BaseModel):
    id: int
    user_id: int
    user_login: str
    user_name: str
    game_id: int | str
    game_name: str
    type: str
    title: str
    viewer_count: int
    started_at: str
    language: str
    thumbnail_url: str
    tag_ids: list
    is_mature: bool
