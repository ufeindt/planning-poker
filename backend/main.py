from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.poll import (
    UserAddRequest,
    Poll,
    PollCreateRequest,
    VoteUpdateRequest,
    add_user_to_poll,
    fetch_poll,
    insert_poll,
    update_vote
)

origins = [
    "http://localhost",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/poll")
async def get_poll():
    return {"message": "Hello World"}


@app.post("/poll")
async def create_poll(request: PollCreateRequest) -> Poll:
    poll = insert_poll(request)
    return poll


@app.get("/poll/{poll_id}")
async def get_poll_by_poll_id(poll_id: str) -> Poll:
    poll = fetch_poll(poll_id)
    poll.pop("_id")
    return poll


@app.post("/poll/{poll_id}")
async def create_poll_user(poll_id: str, request: UserAddRequest) -> str:
    result = add_user_to_poll(poll_id, request.name)
    return result.user_id


@app.get("/poll/{poll_id}/user/{user_id}")
async def get_poll_by_poll_and_user_id(poll_id: str, user_id: str) -> Poll:
    poll = fetch_poll(poll_id)
    poll.pop("_id")

    if user_id not in poll["participants"]:
        raise HTTPException(status_code=404, detail="User not found.")
    return poll


@app.put("/poll/{poll_id}/user/{user_id}")
async def update_user_vote(poll_id: str, user_id: str, request: VoteUpdateRequest) -> Poll:
    try:
        poll = update_vote(poll_id, user_id, request.vote)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args)

    poll.pop("_id")
    return poll