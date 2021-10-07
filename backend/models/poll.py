from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel
from pymongo import MongoClient

from lib.utils import b64_id, convert_b64_id_to_object_id
from models.user import User, VoteStatus
from settings import MONGO_HOST, MONGO_PASS, MONGO_USER

uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}"


class PollStatus(str, Enum):
    VOTES_PENDING = "votes pending"
    VOTES_RECEIVED = "votes received"
    POLL_REVEALED = "poll revealed"


class Poll(BaseModel):
    poll_id: Optional[str]
    description: str
    owner_id: str
    poll_status: PollStatus = PollStatus.VOTES_PENDING
    participants: Dict[str, User]


class PollCreateRequest(BaseModel):
    name: str
    description: str


class UserAddRequest(BaseModel):
    name: str


class UserAddResult(BaseModel):
    user_id: str
    poll: Poll


class VoteUpdateRequest(BaseModel):
    vote: Optional[int]


def insert_poll(request: PollCreateRequest) -> Poll:
    """
    Create a new poll and insert it into the DB.
    """
    user_owner = User(user_id=b64_id(), name=request.name)

    poll = Poll(
        description=request.description,
        owner_id=user_owner.user_id,
        participants={user_owner.user_id: user_owner},
    )

    with MongoClient(uri) as client:
        collection = client.planning_poker.polls
        result_insert = collection.insert_one(poll.dict())

        # Create a shorter version of the ObjectId
        poll = Poll(
            poll_id=b64_id(result_insert.inserted_id),
            **poll.dict(exclude={"poll_id"}),
        )
        result_update = collection.update_one(
            {"_id": result_insert.inserted_id},
            {"$set": {"poll_id": poll.poll_id}},
        )

    return poll


def fetch_poll(poll_id: str) -> Poll:
    """
    Fetch an existing poll.
    """
    poll_object_id = convert_b64_id_to_object_id(poll_id)
    with MongoClient(uri) as client:
        collection = client.planning_poker.polls
        poll = collection.find_one({"_id": poll_object_id})

    return poll


def add_user_to_poll(poll_id: str, name: str) -> UserAddResult:
    """
    Add a new user to the participants of an existing poll.

    :param poll_id: The existing poll's poll_id.
    :param name: The new user's name.
    :return: The new user's user_id and the updated poll.
    """
    poll = fetch_poll(poll_id)
    new_user = User(user_id=b64_id(), name=name)
    poll["participants"][new_user.user_id] = new_user.dict()
    poll["poll_status"] = PollStatus.VOTES_PENDING

    with MongoClient(uri) as client:
        collection = client.planning_poker.polls
        collection.replace_one({"_id": poll["_id"]}, poll)

    return UserAddResult(user_id=new_user.user_id, poll=poll)


def update_vote(poll_id: str, user_id: str, vote: int = None) -> Poll:
    """
    Update an existing user's vote and return the updated poll.

    :param poll_id: The existing poll's poll_id.
    :param user_id: The existing user's user_id.
    :param vote: The user's vote. (Optional: if None, the vote will be
        reset.)
    :return: The update poll.
    """
    poll = fetch_poll(poll_id)
    if poll is None:
        raise ValueError("Poll not found.")
    if user_id not in poll["participants"]:
        raise ValueError("User not found.")

    poll["participants"][user_id]["vote"] = vote
    if vote is None:
        poll["participants"][user_id]["vote_status"] = VoteStatus.PENDING
        poll["poll_status"] = PollStatus.VOTES_PENDING
    else:
        poll["participants"][user_id]["vote_status"] = VoteStatus.VOTED
        if all(
            [
                user["vote_status"] == VoteStatus.VOTED
                for user in poll["participants"].values()
            ]
        ):
            poll["poll_status"] = PollStatus.VOTES_RECEIVED

        with MongoClient(uri) as client:
            collection = client.planning_poker.polls
            collection.replace_one({"_id": poll["_id"]}, poll)

    return poll
