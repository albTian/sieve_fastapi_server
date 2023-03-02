from sqlalchemy.orm import Session
import json
from . import models, schemas

# gets all videos
def get_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Video).offset(skip).limit(limit).all()

# get video by id
def get_video_by_id(db: Session, id: str) -> models.Video:
    return db.query(models.Video).filter(models.Video.id == id).first()
    
# put a new video
def put_video(db: Session, item: schemas.VideoCreate, status: str):
    db_item = models.Video(**item.dict(), status = status, data="")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# update video status
def update_video_status(db: Session, id: str, status: str):
    # can probably make this smarter so it doesn't do a full query each time
    db_video: models.Video = get_video_by_id(db, id)
    db_video.status = status
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return

def update_video_data(db: Session, id: str, data: object):
    db_video: models.Video = get_video_by_id(db, id)
    db_video.data = json.dumps(data)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return
