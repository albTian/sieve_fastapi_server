# Sieve takehome challenge
This is my submission for the Sieve take home challenge!

### How to run
`pip install -r requirements.txt`
`python3 -m uvicorn main:app`

### Technical decisions
- Instead of Flask, I used FastAPI. I've used FastAPI before and knew it could handle queueing jobs very easily, so a large part of the project would be handled there
- For data storage, I opted to use an internal sql app (`sql_app`) using sqlalchemy as the orm and an in memory database. The frame data would simply be parsed with `json`
- For ML processing, the YOLO and SORT code I began to write until I found [sieve's version](https://github.com/sieve-community/examples/tree/main/yolo_object_tracking). I did most of my work in `playground.ipynb` before putting it into `ml_processing.py`

### Challenges
- I finished the core API on Wednesday, but really wanted a Frontend interface to go along with it to easily test, so I'm trying to deploy the server. I've never deployed a webserver manually (Docker, ECS) and it's been fun learning.
- Especially since the packages (and thus docker image) are quite large, I ran into issues on AWS with CPU and memory allocation
- I'm still working on it and would like to deploy it, but for the sake of my time and yours the core API is finished :)