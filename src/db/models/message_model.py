from tortoise import fields

from core.enums import AttachmentType
from db.models.base import TimestampMixin


class MessageStatus(TimestampMixin):
    id = fields.IntField(pk=True)

    message = fields.ForeignKeyField("models.Message", related_name="read_by")
    user = fields.ForeignKeyField("models.User", related_name="read_messages")

    read_at = fields.DatetimeField(null=True, blank=True)
    delivered_at = fields.DatetimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"MessageStatus(msg={self.message.id}, user={self.user.id})"

    class Meta:
        table = "messages_status"
        unique_together = ("message", "user")
        indexes = [("message_id", "user_id")]


class Message(TimestampMixin):
    id = fields.IntField(pk=True)

    sender = fields.ForeignKeyField(
        'models.User', related_name='sent_messages'
    )
    chat = fields.ForeignKeyField(
        'models.Chat', related_name='messages', null=True
    )
    channel = fields.ForeignKeyField(
        'models.Channel', related_name='messages', null=True
    )

    text = fields.TextField(null=True)
    is_reply = fields.BooleanField(default=False)
    reply_to = fields.ForeignKeyField(
        'models.Message', related_name='replies', null=True
    )

    is_read = fields.BooleanField(default=False)

    class Meta:
        table = "messages_message"


    def __str__(self) -> str:
        return f"Message #{self.id}"


class Attachment(TimestampMixin):
    id = fields.IntField(pk=True)

    message = fields.ForeignKeyField('models.Message', related_name='attachments')
    file_url = fields.CharField(max_length=1024)
    file_type = fields.CharEnumField(AttachmentType)

    file_name = fields.CharField(max_length=255, null=True)
    mime_type = fields.CharField(max_length=100, null=True)

    class Meta:
        table = "messages_attachment"

    def __str__(self) -> str:
        return f"Attachment #{self.id}"
