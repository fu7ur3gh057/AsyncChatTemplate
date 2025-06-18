from enum import Enum


class AttachmentType(str, Enum):
    IMAGE = "image"
    FILE = "file"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"

