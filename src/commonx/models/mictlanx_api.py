from pydantic import BaseModel,Field
from typing import Optional
import datetime as DT

class UserProfileModel(BaseModel):
    user_id: str
    avatar_url: str
    bio: Optional[str] = ""
    language:Optional[str] = "en"
    color: Optional[str] = "blue"
    local_path: Optional[str] = None
    created_at: Optional[DT.datetime] = Field(default_factory=lambda: DT.datetime.now(DT.timezone.utc))
    updated_at: Optional[DT.datetime] = Field(default_factory=lambda: DT.datetime.now(DT.timezone.utc))