from typing import Dict,Set,Optional,List,Generic,TypeVar
from pydantic import BaseModel
T = TypeVar("T")

class AuthAttemptDTO(BaseModel):
    username: str
    password: str
    scope: str
    expiration: Optional[str] = "1h"
    renew_token: Optional[bool] = False

class PaginatedResponseDTO(BaseModel, Generic[T]):
    items: List[T]
    total_count: int
    page: int
    page_size: int
    total_pages: int

class DashboardFilterDTO(BaseModel):
    page: int = 1
    page_size: int = 10
    
class CheckDTO(BaseModel):
    # principal_id:str
    resource_id:str
    permissions:List[str]
    
class GrantsDTO(BaseModel):
    grants:Dict[str,Dict[str,Set]]
    role:Optional[str]=""


class GroupDetailDTO(BaseModel):
    id:str
    name:str
    my_role:str

class ResourceDetailDTO(BaseModel):
    resource_id:str
    access_source:str
    permissions:Set[str]

class UserDashboardViewDTO(BaseModel):
    user_id: str
    groups: List[GroupDetailDTO]
    owned_resources: PaginatedResponseDTO[ResourceDetailDTO] # Updated type
    shared_resources: PaginatedResponseDTO[ResourceDetailDTO] # Updated type

class AddOrDeleteMembersToGroupDTO(BaseModel):
    members:List[str]

class GrantOrRevokePermissionDTO(BaseModel):
    principal_id:str
    principal_type:Optional[str]= None  # "user" | "group"
    resource_id:str
    permissions:List[str]

class ClaimResourceDTO(BaseModel):
    resource_id:str
    # is_owner:bool = False

class LogoutDTO(BaseModel):
    access_token:str
    username:str


class EnableOrDisableUserDTO(BaseModel):
    username:str


class CreateUserDTO(BaseModel):
    username:str
    first_name:str
    last_name:str
    email:str
    password:str
    profile_photo:str=""

class DeleteLicenseDTO(BaseModel):
    username:str
    scope:str
    force: Optional[bool] = True
class SelfDeleteLicenseDTO(BaseModel):
    token: str
    tmp_secret_key:str
    username:str
    scope:str
    force: Optional[bool] = True
class DeletedLicenseResponseDTO(BaseModel):
    ok:bool

class AssignLicenseDTO(BaseModel):
    username: str
    scope:str
    expires_in:str
    force: Optional[bool] = True

class AssignLicenseResponseDTO(BaseModel):
    expires_at: str
    ok:bool
    
class UpdateUserPasswordDTO(BaseModel):
    username:str
    password: str
class UpdateUserPasswordResponseDTO(BaseModel):
    ok:bool

class CreateScopeDTO(BaseModel):
    name:str
class CreatedScopeResponseDTO(BaseModel):
    name:str

class AssignScopeDTO(BaseModel):
    name:str
    username:str
class AssignedScopeResponseDTO(BaseModel):
    name:str
    username:str
    ok:bool

class CreatedUserResponseDTO(BaseModel):
    key: str

class AuthDTO(BaseModel):
    username:str
    password:str
    scope: Optional[str] = "Xolo"
    expiration: Optional[str] = "15min",
    renew_token: Optional[bool] = False


    
class VerifyDTO(BaseModel):
    access_token:str
    username:str
    secret:str
    
class AuthenticatedDTO(BaseModel):
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
    key:str 
    username:str
    first_name:str
    last_name:str
    email:str
    profile_photo:str
    disabled:Optional[bool]=False

class CreateGroupDTO(BaseModel):
    name:str
    description:Optional[str]=""