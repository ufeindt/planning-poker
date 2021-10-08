from enum import Enum
from typing import Dict, Optional
import json

from fastapi import WebSocket
from fastapi.logger import logger
from pydantic import BaseModel

from models.poll import Poll, fetch_poll, reset_poll, reveal_poll_result, update_vote


class WebsocketMessageAction(str, Enum):
    CAST_VOTE = "cast vote"
    RESET_VOTE = "reset vote"
    RESET_POLL = "reset poll"
    REVEAL_POLL = "reveal poll"


class WebsocketMessage(BaseModel):
    poll_id: str
    user_id: str
    action: WebsocketMessageAction
    vote: Optional[int]


class WebsocketResponseType(str, Enum):
    ERROR = "error"
    UPDATE = "update"


class WebsocketResponse(BaseModel):
    response_type: WebsocketResponseType
    message: Optional[str]
    poll: Optional[Poll]


class WebsocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, poll_id: str, user_id: str):
        await websocket.accept()
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = {}
        self.active_connections[poll_id][user_id] = websocket

        poll = fetch_poll(poll_id)
        await self.respond(
            poll_id,
            WebsocketResponse(
                response_type=WebsocketResponseType.UPDATE, poll=poll
            ),
        )

    def disconnect(self, poll_id: str, user_id: str):
        self.active_connections.get(poll_id, {}).pop(user_id)
        if self.active_connections.get(poll_id) == {}:
            self.active_connections.pop(poll_id)

    async def process_message(self, message: WebsocketMessage):
        if message.action == WebsocketMessageAction.CAST_VOTE:
            poll = update_vote(message.poll_id, message.user_id, message.vote)
        elif message.action == WebsocketMessageAction.RESET_VOTE:
            poll = update_vote(message.poll_id, message.user_id, None)
        elif message.action == WebsocketMessageAction.RESET_POLL:
            try:
                poll = reset_poll(message.poll_id, message.user_id)
            except ValueError as e:
                await self.respond(
                    message.poll_id,
                    WebsocketResponse(
                        response_type=WebsocketResponseType.ERROR, message=e
                    ),
                )
        elif message.action == WebsocketMessageAction.REVEAL_POLL:
            try:
                poll = reveal_poll_result(message.poll_id, message.user_id)
            except ValueError as e:
                await self.respond(
                    message.poll_id,
                    WebsocketResponse(
                        response_type=WebsocketResponseType.ERROR, message=e
                    ),
                )
        else:
            await self.respond(
                message.poll_id,
                WebsocketResponse(
                    response_type=WebsocketResponseType.ERROR,
                    message=f"Action unknown: {message.action}",
                ),
            )

        await self.respond(
            message.poll_id,
            WebsocketResponse(
                response_type=WebsocketResponseType.UPDATE, poll=poll
            ),
        )

    async def respond(self, poll_id: str, response: WebsocketResponse):
        for user_id, connection in self.active_connections[poll_id].items():
            logger.info(f"Sending message to {user_id}")
            print(f"Sending message to {user_id}") 
            await connection.send_text(json.dumps(response.dict()))
