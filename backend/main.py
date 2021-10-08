import json

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from lib.websockets import WebsocketManager, WebsocketMessage
from models.poll import (
    UserAddRequest,
    Poll,
    PollCreateRequest,
    VoteUpdateRequest,
    add_user_to_poll,
    fetch_poll,
    insert_poll,
    update_vote,
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

ws_manager = WebsocketManager()


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
async def update_user_vote(
    poll_id: str, user_id: str, request: VoteUpdateRequest
) -> Poll:
    try:
        poll = update_vote(poll_id, user_id, request.vote)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args)

    poll.pop("_id")
    return poll


@app.websocket("/ws/poll/{poll_id}/user/{user_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: str, user_id: str):
    await ws_manager.connect(websocket, poll_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # await ws_manager.send_personal_message(f"OK", websocket)
            data = WebsocketMessage(**json.loads(data))
            await ws_manager.process_message(data)
    except WebSocketDisconnect:
        ws_manager.disconnect(poll_id, user_id)