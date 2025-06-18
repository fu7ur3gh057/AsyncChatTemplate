from tortoise import fields
from .base import TimestampMixin
from .user_model import User


class Chat(TimestampMixin):
    id = fields.IntField(pk=True)
    members: fields.ManyToManyRelation[User] = fields.ManyToManyField(
        "models.User", related_name="chats", through="chat_members"
    )

    class Meta:
        table = "chats_chat"

    def __str__(self):
        return f"Chat #{self.id}"
