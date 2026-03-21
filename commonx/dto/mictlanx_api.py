from pydantic import BaseModel,EmailStr,ConfigDict,model_validator
from typing import Optional,Dict,List
from commonx.dto.xolo import UserDTO
from commonx.enums.mictlanx_api import NodeType
import humanfriendly as HF



class FileXNodeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    node_id: str
    name: str
    extension: Optional[str] = None
    ntype: NodeType
    size_bytes: int
    size_str: str 
    parent_id: Optional[str] = None
    children: List['FileXNodeDTO'] = []
    bucket_id: Optional[str] = None
    ball_id: Optional[str] = None
    key: Optional[str] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    view_mode: Optional[str] = None
    thumbnail_url: Optional[str] = None
    ancestors: Optional[List[str]] = []
    
    @model_validator(mode='after')
    def verify_size_str(self):
        self.size_str = HF.format_size(self.size_bytes)
        return self

class UploadXNodeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str
    extension: Optional[str] = None
    ntype: NodeType
    checksum: Optional[str] = None
    size_bytes: int
    parent_id: Optional[str] = None
    tags: Optional[List[str]] = None
    ancestor_ids: Optional[List[str]] = None
    # bucket_id: Optional[str] = None
    # ball_id: Optional[str] = None
    # key: Optional[str] = None
    # color: Optional[str] = None
    # icon: Optional[str] = None
    # view_mode: Optional[str] = None
    # thumbnail_url: Optional[str] = None



class CreateUsersProfilesDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    user_id: str
    avatar_url: str
    bio: Optional[str] = ""
    language:Optional[str] = "en"
    color: Optional[str] = "blue"
    local_path: Optional[str] = None
class UserProfileDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    user_id:str
    avatar_url:str
    bio:Optional[str]=""
    language:Optional[str]="en"
    color:Optional[str]="blue"
    local_path:Optional[str]=None


class UserProfileAndUserDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    profile:UserProfileDTO
    user:UserDTO

class AuthenticatedUserProfileDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    first_name:str
    last_name:str
    email:EmailStr
    profile_photo:str
    access_token:str
    metadata:Dict[str,str]
    temporal_secret:str
    profile:UserProfileDTO

class SignUpDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    profile_photo:str=""