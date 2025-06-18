from tortoise import models, fields
from datetime import datetime


class TimestampMixin(models.Model):
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
