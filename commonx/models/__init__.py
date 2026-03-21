
from pydantic import BaseModel, Field
import datetime as DateTime

class TimestampMixin(BaseModel):
    """
    A reusable helper. Any class that inherits from this
    will automatically get 'created_at' and 'updated_at' fields.
    """
    created_at:DateTime.datetime = Field(default_factory=lambda: DateTime.datetime.now(DateTime.timezone.utc))
    updated_at:DateTime.datetime = Field(default_factory=lambda: DateTime.datetime.now(DateTime.timezone.utc))