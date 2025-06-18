from tortoise import fields
from .base import TimestampMixin


class User(TimestampMixin):
    id = fields.IntField(pk=True)
    external_id = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=255, unique=True, null=True)

    class Meta:
        table = "users_user"

    def __str__(self):
        return self.external_id
