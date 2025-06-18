import uuid

from tortoise import fields

from db.models.base import TimestampMixin


def generate_token() -> str:
    return str(uuid.uuid4())[:512]


class KeyModel(TimestampMixin):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=512, default=lambda: generate_token())
    app_name = fields.CharField(max_length=100)
    domain = fields.CharField(max_length=100, null=True)
