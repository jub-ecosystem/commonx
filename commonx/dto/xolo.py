from typing import Dict,Set,Optional,List,Generic,TypeVar
from pydantic import BaseModel,ConfigDict
T = TypeVar("T")

class AuthAttemptDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str
    password: str
    scope: str
    expiration: Optional[str] = "1h"
    renew_token: Optional[bool] = False

class PaginatedResponseDTO(BaseModel, Generic[T]):
    model_config = ConfigDict(str_strip_whitespace=True)
    items: List[T]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class DashboardFilterDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    page: int = 1
    page_size: int = 10
    
class CheckDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    resource_id:str
    permissions:List[str]
    
class GrantsDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    grants:Dict[str,Dict[str,Set]]
    role:Optional[str]=""


class GroupDetailDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id:str
    name:str
    my_role:str

class ResourceDetailDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    resource_id:str
    access_source:str
    permissions:Set[str]

class UsersResourcesDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    user_id: str
    groups: List[GroupDetailDTO]
    owned_resources: PaginatedResponseDTO[ResourceDetailDTO] # Updated type
    shared_resources: PaginatedResponseDTO[ResourceDetailDTO] # Updated type

class AddOrDeleteMembersToGroupDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    members:List[str]

class GrantOrRevokePermissionDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    principal_id:str
    principal_type:Optional[str]= None  # "user" | "group"
    resource_id:str
    permissions:List[str]

class ClaimResourceDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    resource_id:str
    # is_owner:bool = False

class LogoutDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    access_token:str
    username:str


class EnableOrDisableUserDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str


class CreateUserDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    first_name:str
    last_name:str
    email:str
    password:str
    profile_photo:str=""

class SignUpDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    first_name:str
    last_name:str
    email:str
    password:str
    profile_photo:str=""
    scope: str
    expiration: Optional[str] = "1h"

class DeleteLicenseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    scope:str
    force: Optional[bool] = True
class SelfDeleteLicenseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    token: str
    tmp_secret_key:str
    username:str
    scope:str
    force: Optional[bool] = True
class DeletedLicenseResponseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ok:bool

class AssignLicenseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str
    scope:str
    expires_in:str
    force: Optional[bool] = True

class AssignLicenseResponseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    expires_at: str
    ok:bool
    
class UpdateUserPasswordDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    password: str
class UpdateUserPasswordResponseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ok:bool

class CreateScopeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name:str
class CreatedScopeResponseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name:str

class AssignScopeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name:str
    username:str
class AssignedScopeResponseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name:str
    username:str
    ok:bool

class CreatedUserResponseDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    key: str

class AuthDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    password:str
    scope: Optional[str] = "Xolo"
    expiration: Optional[str] = "15min",
    renew_token: Optional[bool] = False


    
class VerifyDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    access_token:str
    username:str
    secret:str
    
class AuthenticatedDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username:str
    first_name:str
    last_name:str
    email:str
    profile_photo:str
    access_token:str
    metadata:Dict[str,str]
    temporal_secret:str
    user_id: Optional[str]=None

class UserDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    key:str 
    username:str
    first_name:str
    last_name:str
    email:str
    profile_photo:str
    disabled:Optional[bool]=False

class CreateGroupDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name:str
    description:Optional[str]=""