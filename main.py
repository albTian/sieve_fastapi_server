from typing import List
from fastapi import FastAPI, BackgroundTasks
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from ml_processing import ml_process_video
import json


from sql_app import crud, models, schemas, database
engine, SessionLocal = database.engine, database.SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# get all videos
@app.get("/list")
async def list_videos(db: Session = Depends(get_db)):
    # put entry into DB with status "queued"
    videos = crud.get_videos(db)
    return videos

# get the status of video with id
@app.get("/status/{video_id}")
async def video_status(video_id: str, db: Session = Depends(get_db)):
    video: models.Video = crud.get_video_by_id(db, video_id)
    return f"No video with id: {video_id}" if not video else video.status 

# get the data of video with id
@app.get("/query/{video_id}")
async def video_status(video_id: str, db: Session = Depends(get_db)):
    video: models.Video = crud.get_video_by_id(db, video_id)
    return f"No video with id: {video_id}" if not video else json.loads(video.data)

# endpoint to create new video to be processed
@app.post("/push")
async def push_video(video_item: schemas.VideoCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # put entry into DB with status "queued"
    video_to_process = crud.put_video(db, video_item, "queued")
    # add it to background_tasks
    background_tasks.add_task(process_video, video_to_process, db)
    return video_to_process.id

# processes video and updates database while doing so. Will be called with add_task, must be one atomic action
# id must be generated before this function
def process_video(video_to_process: models.Video, db: Session = Depends(get_db)):
    # 1. updates status to "processing"
    id = video_to_process.id
    crud.update_video_status(db, id, "processing")

    # TODO: ML PROCESSING HERE
    # TODO: add data to table here
    ml_data = ml_process_video(video_to_process.source_url)
    crud.update_video_data(db, id, ml_data)

    # n. update status to "finished"
    crud.update_video_status(db, id, "finished")
    return 0