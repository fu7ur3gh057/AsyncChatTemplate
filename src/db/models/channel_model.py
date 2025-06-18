from tortoise import fields
from .base import TimestampMixin
from .user_model import User


class Channel(TimestampMixin):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    icon_url = fields.CharField(max_length=512, null=True)

    members: fields.ManyToManyRelation[User] = fields.ManyToManyField(
        "models.User", related_name="channels", through="channel_members"
    )

    class Meta:
        table = "channels_channel"

    def __str__(self):
        return f"Channel {self.title}"
