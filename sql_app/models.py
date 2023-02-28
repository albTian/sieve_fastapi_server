from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

# During local testing: Make sure to delete sql_app.db if changing columns (!!!)
class Video(Base):
    __tablename__ = "videos"

    # uniquely generated uuid
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, index=True)
    source_url = Column(String, index=True)
    status = Column(String, index=True)