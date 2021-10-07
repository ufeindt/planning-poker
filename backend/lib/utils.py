from bson.objectid import ObjectId
from base64 import urlsafe_b64decode, urlsafe_b64encode


def b64_id(object_id: ObjectId = None) -> str:
    """
    Shorten a MongoDB ObjectId pattern buy reversing it, so IDs look
    less alike, and converting it to base 64 to shorten it.

    Alternatively if the no object_id is passed, generate a random ID.

    :param object_id: ObjectId as used by MongoDB.
    :return: String of the shorter base-64 ID.
    """
    if object_id is None:
        object_id = ObjectId()

    hex_id = str(object_id)[::-1]
    b64_id = urlsafe_b64encode(bytes.fromhex(hex_id)).decode()
    return b64_id


def convert_b64_id_to_object_id(b64_id: str) -> ObjectId:
    """
    Inverse of `b64_id()`.

    :param b64_id: Base-64 id.
    :return: The ObjectId it originated from.
    """
    return ObjectId(urlsafe_b64decode(b64_id).hex()[::-1])