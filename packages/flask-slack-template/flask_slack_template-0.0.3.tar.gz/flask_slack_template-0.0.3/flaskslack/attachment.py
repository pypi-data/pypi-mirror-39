from dataclasses import dataclass, field, asdict
from typing import List


# TODO build out all dataclasses according to Slack API documentation
# (which is just all over the place and hard to consolidate)

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


@dataclass
class Action:
    """
    https://api.slack.com/docs/message-buttons
    """
    name: str = None
    text: str = None
    type: str = "button"
    value: str = None


@dataclass
class ButtonAttachment(Attachment):
    """
    Data class for Attachments with buttons
    https://api.slack.com/docs/interactive-message-field-guide
    """
    text: str = None
    fallback: str = "default fallback"
    callback_id: str = None
    color: str = "#123456"
    attachment_type: str = "default"
    actions: List[Action] = None
    confirm = None  # TODO confirm textbox
    footer: str = None

    def asdict(self):
        return asdict(self)
