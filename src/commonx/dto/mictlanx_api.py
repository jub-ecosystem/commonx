from pydantic import BaseModel,EmailStr,Field
from typing import Optional,Dict
from commonx.dto.xolo import UserDTO
class CreateUsersProfilesDTO(BaseModel):
    user_id: str
    avatar_url: str
    bio: Optional[str] = ""
    language:Optional[str] = "en"
    color: Optional[str] = "blue"
    local_path: Optional[str] = None
class UserProfileDTO(BaseModel):
    user_id:str
    avatar_url:str
    bio:Optional[str]=""
    language:Optional[str]="en"
    color:Optional[str]="blue"
    local_path:Optional[str]=None


class UserProfileAndUserDTO(BaseModel):
    profile:UserProfileDTO
    user:UserDTO

class AuthenticatedUserProfileDTO(BaseModel):
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
    username:str
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    profile_photo:str=""