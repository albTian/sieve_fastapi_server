from typing import List
from fastapi import FastAPI, BackgroundTasks
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session


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
    # assume entry is already in DB. updates status to "processing"
    crud.update_video_status(db, video_to_process.id, "processing")

    # n. update status to "finished"
    crud.update_video_status(db, video_to_process.id, "finished")
    return 0