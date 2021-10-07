from bson.objectid import ObjectId
from enum import Enum
from typing import Optional

from pydantic import BaseModel

class VoteStatus(str, Enum):
    PENDING = "pending"
    VOTED = "voted"


class User(BaseModel):
    user_id: str
    name: str
    vote: Optional[int]
    vote_status: VoteStatus = VoteStatus.PENDING

