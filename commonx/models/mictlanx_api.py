from pydantic import ConfigDict,Field,field_validator
from typing import Optional,List
from commonx.models import TimestampMixin
import random
from commonx.enums.mictlanx_api import NodeType,NodeStatus
from commonx.helpers import Helpers as H

class UserProfileModel(TimestampMixin):
    model_config = ConfigDict(str_strip_whitespace=True)
    user_id: str
    avatar_url: str = ""
    bio: Optional[str] = ""
    language:Optional[str] = "en"
    color: Optional[str] = "blue"
    local_path: Optional[str] = None


    def from_name(self,name:str) -> 'UserProfileModel':
        color = "{:06x}".format(random.randint(0, 0xFFFFFF)).upper()
        self.color = f"#{color}"
        if not self.avatar_url or self.avatar_url.strip() == "":
            self.avatar_url = f"https://ui-avatars.com/api/?name={name}&background={color}&color=fff"
        return self


class UserSettingsModel(TimestampMixin):
    model_config = ConfigDict(str_strip_whitespace=True)
    user_id: str
    email_notifications: bool = True
    sms_notifications: bool = False
    dark_mode: bool = False


# --- Enums ---


# --- Sub-Models (Components) ---

class StorageRef(TimestampMixin):
    """
    Links the Logical Node to the Physical Storage (Sled/MinIO/S3).
    """
    model_config = ConfigDict(populate_by_name=True,str_strip_whitespace=True)

    bucket_id: str 
    ball_id: Optional[str] = None
    size_bytes: int = 0
    checksum: Optional[str] = None

class Presentation(TimestampMixin):
    """
    UI-specific attributes. 
    Allows users to customize how their 'Underworld' looks.
    """
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    color: Optional[str] = None    # e.g. "#FF5722" for folder color
    icon: Optional[str] = None     # e.g. "mdi-file-document"
    view_mode: str = "grid"        # "grid" or "list" preference for this folder
    thumbnail_url: Optional[str] = None # For images/videos

# --- The Main Model ---

class XNode(TimestampMixin):
    """
    Represents both Files and Folders in the hierarchy.
    """
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    # tree_id:Optional[str] = None
    node_id: str
    # Hierarchy Pointers
    parent_id: Optional[str] = None  # None ONLY for the Root Folder ("MyRealm")
    owner_id: str                    # The User ID
    
    # Breadcrumbs / Navigation Optimization
    # List of ancestor IDs. e.g. [root_id, folder_a_id, folder_b_id]
    # Allows finding all children in a subtree quickly.
    ancestors: List[str] = Field(default_factory=list)

    # Basic Info
    name: str
    type: NodeType
    extension: Optional[str] = None # "pdf", "jpg" (Null for folders)
    mime_type: Optional[str] = None # "application/json" (Null for folders)
    
    # State
    status: NodeStatus = NodeStatus.ACTIVE
    is_starred: bool = False
    is_shared: bool = False # Fast flag to show "Shared" icon without querying ACL
    
    # Components
    storage: Optional[StorageRef] = None # None for Folders if they are purely logical
    presentation: Presentation = Field(default_factory=Presentation)
    
    # Arbitrary User Tags (e.g., "Work", "Urgent")
    tags: List[str] = Field(default_factory=list)

    @property
    def is_folder(self) -> bool:
        return self.type == NodeType.FOLDER
    
    @field_validator("parent_id",mode="before")
    @classmethod
    def sanitize_parent_id(cls, v:Optional[str])->Optional[str]:
        return H.sanitize_null_id_none(v)
        # if v is None:
        #     return v
        
        # if not isinstance(v,str):
        #     raise ValueError("parent_id must be a string or None")
        # null_values = {"", "null", "none", "undefined", "nil"}
        # v_sanitized = v.strip()
        # if v_sanitized.lower() in null_values:
        #     return None
        # return v_sanitized

