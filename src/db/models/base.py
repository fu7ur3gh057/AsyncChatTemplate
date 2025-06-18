from datetime import datetime, timezone

from tortoise import models, fields


class TimestampMixin(models.Model):
    created_at = fields.DatetimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
