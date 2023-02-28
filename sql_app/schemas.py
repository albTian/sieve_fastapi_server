from typing import List
from pydantic import BaseModel, AnyUrl

class VideoBase(BaseModel):
    source_name: str
    source_url: AnyUrl

class VideoCreate(VideoBase):
    pass

# During local testing: Make sure to delete sql_app.db if changing columns (!!!)
class VideoItem(VideoBase):
    id: int
    status: str

    class Config:
        orm_mode = True