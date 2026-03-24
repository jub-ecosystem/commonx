#xoloapi/models/__init__.py
import random
from pydantic import EmailStr,model_validator,ConfigDict
from typing import Optional,List
import commonx.enums.xolo as Enums
from commonx.models import TimestampMixin
# from enum import Enum


class LicenseAssignedModel(TimestampMixin):
    username: str
    license: str
    scope: str 
    expires_at:str
class User(TimestampMixin):

    model_config = ConfigDict(str_strip_whitespace=True)
    profile_photo:Optional[str] =  None
    key:str
    first_name:str
    last_name:str
    username:str
    email:EmailStr
    hash_password:str
    disabled:Optional[bool] = False

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @model_validator(mode="before")
    def generate_default_profile_photo(cls, values)->'User':
        first_name = values.get('first_name', '')
        last_name = values.get('last_name', '')

        full_name = f"{first_name.title()}+{last_name.title()}"
        bg_color = "{:06x}".format(random.randint(0, 0xFFFFFF)).upper()
        values['profile_photo'] = (
            f"https://ui-avatars.com/api/?"
            f"name={full_name}&"
            f"background={bg_color}&"
            f"color=fff" # White text
        )
        return values
class SecurityGroup(TimestampMixin):
    """
    Represents the Group entity itself (Metadata).
    """
    model_config = ConfigDict(str_strip_whitespace=True)
    group_id: str
    name: str
    owner_id: str # The user who owns/manages this group
    description: Optional[str] = None

class GroupMember(TimestampMixin):
    """
    The Join Table / Link Collection.
    Maps User <-> Group.
    """
    # id: Optional[str] = Field(alias="_id", default=None)
    model_config = ConfigDict(str_strip_whitespace=True)
    group_id: str
    user_id: str
    
    # Optional: Role *within* the group (e.g., "Member" vs "Moderator")
    role_in_group: str = "member" 

    # class Config:
        # populate_by_name = True

class AccessPolicy(TimestampMixin):
    """
    The permission assignment.
    """
    # id: Optional[str] = Field(alias="_id", default=None)
    model_config = ConfigDict(str_strip_whitespace=True)
    resource_id: str
    principal_id: str # Can be UserID or GroupID
    principal_type: Enums.PrincipalType 
    permissions: List[Enums.Permission]
    is_owner: bool = False


class ScopeModel(TimestampMixin):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str

class ScopeUserModel(TimestampMixin):
    model_config = ConfigDict(str_strip_whitespace=True)
    name:str
    username:str
