from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Field:
    title: str = None
    value: str = None
    short: bool = False


@dataclass
class Attachment:
    fallback: str = "default fallback"
    color: str = "#123456"
    pretext: str = None
    author_name: str = None
    author_link: str = None
    author_icon: str = None
    title: str = None
    title_link: str = None
    text: str = None
    fields: List[Field] = field(default_factory=list)
    image_url: str = None
    thumb_url: str = None
    footer: str = None
    footer_icon: str = None
    ts: int = None  # timestamp

    def asdict(self):
        return asdict(self)
