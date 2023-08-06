from enum import Enum
from io import BytesIO
from mimetypes import guess_all_extensions
from pathlib import Path
from typing import List, FrozenSet, Optional, Dict
from uuid import uuid4

import aiofiles
import magic
import phpserialize
from PIL import Image
from mime import Types


class UploadType(Enum):
    AVATAR = "avatar"
    PHOTO = "photo"
    IMAGE = "image"
    FILE = "file"


RESIZABLE_TYPES = {
    UploadType.AVATAR: frozenset([100, 64, 48, 24]),
    UploadType.PHOTO: frozenset([250]),
    UploadType.IMAGE: frozenset([0]),
}
FORCED_EXTENSIONS = {
    UploadType.AVATAR: "png",
    UploadType.PHOTO: "png",
}
Images = Dict[int, bytes]


def extract_user_id(payload: Optional[bytes]) -> Optional[int]:
    if payload is None:
        return None
    try:
        session = phpserialize.loads(payload)
        return int(session.get("user_id"))
    except (KeyError, ValueError, TypeError):
        return None


def get_resizable_name(upload_type: UploadType, width: int):
    suffix = "" if width == 0 else f"_{width}"
    if upload_type is UploadType.AVATAR:
        return f"{upload_type.value}{suffix}"
    elif upload_type is UploadType.PHOTO:
        return f"{upload_type.value}{suffix}"
    elif upload_type is UploadType.IMAGE:
        return f"{uuid4().hex}{suffix}"
    else:
        return upload_type.value


def get_path_chunks(user_id: int) -> List[str]:
    user_id_padded = str(user_id).zfill(8)
    return [user_id_padded[i:i + 4] for i in range(0, len(user_id_padded), 4)]


async def save_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(path.as_posix(), "wb") as f:
        await f.write(data)


def sniff_extension(data: bytes) -> str:
    raw_mime = magic.from_buffer(data[:1024], mime=True)
    exact_mimes = Types[raw_mime]
    rough_mimes = guess_all_extensions(raw_mime)
    if exact_mimes:
        return exact_mimes[0].extensions[0]
    elif rough_mimes:
        return rough_mimes[0][1:]
    else:
        return "bin"


def resize_image(data: bytes, widths: FrozenSet[int], extension: str) -> Optional[Images]:
    try:
        img: Image.Image = Image.open(BytesIO(data))
    except IOError:
        return None

    result = {}
    for width in widths:
        if width == 0:
            result[width] = data
        else:
            with BytesIO() as b:
                height = int(float(img.height) * (width / float(img.width)))
                img.resize((width, height), Image.LANCZOS).save(b, extension)
                result[width] = b.getvalue()

    return result
