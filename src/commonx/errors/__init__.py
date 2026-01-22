from abc import ABC,abstractmethod
from typing import Optional,Dict,Any
from option import Err
from fastapi import HTTPException
from pydantic import BaseModel


ERROR_CODES = {
    "X.UNKNOWN": -1,
    "X.ERROR": 0,
    "X.USER_NOT_FOUND": 1001,
    "X.USER_ALREADY_EXISTS": 1002,
    "X.UNAUTHORIZED": 1003,
    "X.INVALID_CREDENTIALS": 1004,
    "X.TOKEN_EXPIRED": 1005,
    "X.ACCESS_DENIED": 1006,
    "X.CREATION_ERROR": 1007,
    "X.NOT_FOUND": 1008,
    "X.ALREADY_EXISTS": 1009,
    "X.SERVER_ERROR": 1010,
    "X.INVALID_LICENSE": 1011,
    "X.UPLOAD_FAILED": 2001,
    "X.DOWNLOAD_FAILED": 2002,
}


class ErrorDetail(BaseModel):
    http_status: int
    code: Optional[str] = "X.ERROR"
    code_int: Optional[int] = 0
    detail: str
    raw_error: Optional[str] = None
    metadata:Optional[Dict[str,Any]] = {}



class XError(Exception,ABC):
    def __init__(self, *args,detail:str,raw_detail:Optional[str]=None,headers:Optional[dict]={},metadata:Dict[str,Any]={}):
        super().__init__(*args)
        self._detail = detail
        self._headers = headers
        self._raw_detail = raw_detail
        self.metadata = metadata
    @property
    @abstractmethod
    def status_code(self)->int:
        return 500
    @property
    @abstractmethod
    def detail(self) -> ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self._raw_detail,
            metadata    = self.metadata
        )
    @property
    @abstractmethod
    def raw_detail(self) -> Optional[str]:
        return self._raw_detail
    @property
    @abstractmethod
    def code(self) -> Optional[str]:
        return "X.ERROR"
    
    @property
    @abstractmethod
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,-1)
    
    @property
    @abstractmethod
    def headers(self) -> Optional[dict]:
        return self._headers
    
    def to_http_exception(self):
        return HTTPException(
            status_code = self.status_code,
            detail      = self.detail.model_dump()
        )
    @staticmethod
    def from_exception(exc:Exception)->'XError':
        e = UnknownError(str(exc))
        return e

    @staticmethod
    def from_exception_safe( exc: Exception) -> 'XError':
        e = UnknownError(raw_detail=str(exc))
        return Err(e)
    
    @staticmethod
    def from_code_safe(code:str, *args, **kwargs) :
        error_class = {
            "X.UNKNOWN": UnknownError,
            "X.CREATION_ERROR": CreationError,
            "X.ACCESS_DENIED": AccessDenied,
            "X.FAILED_TO_REMOVE_OWNER": FailedToRemoveOwner,
            "X.FAILED_TO_CLAIM_RESOURCE": FailedToClaimResource,
            "X.TOKEN_EXPIRED": TokenExpired,
            "X.LICENSE_CREATION_ERROR": LicenseCreationError,
            "X.NOT_FOUND": NotFound,
            "X.ALREADY_EXISTS": AlreadyExists,
            "X.UNAUTHORIZED": Unauthorized,
            "X.UNAUTHORIZED_SCOPE": UnauthorizedScope,
            "X.INVALID_LICENSE": InvalidLicense,
            "X.SERVER_ERROR": ServerError,
            "X.INVALID_CREDENTIALS": InvalidCredentialsError,
        }.get(code, UnknownError)
        return Err(error_class(*args, **kwargs))
    @staticmethod
    def from_code(code:str, *args, **kwargs) -> 'XError':
        error_class = {
            "X.ERROR": UnknownError,
            "X.UNKNOWN": UnknownError,
            "X.CREATION_ERROR": CreationError,
            "X.ACCESS_DENIED": AccessDenied,
            "X.FAILED_TO_REMOVE_OWNER": FailedToRemoveOwner,
            "X.FAILED_TO_CLAIM_RESOURCE": FailedToClaimResource,
            "X.TOKEN_EXPIRED": TokenExpired,
            "X.LICENSE_CREATION_ERROR": LicenseCreationError,
            "X.NOT_FOUND": NotFound,
            "X.ALREADY_EXISTS": AlreadyExists,
            "X.UNAUTHORIZED": Unauthorized,
            "X.UNAUTHORIZED_SCOPE": UnauthorizedScope,
            "X.INVALID_LICENSE": InvalidLicense,
            "X.SERVER_ERROR": ServerError,
            "X.INVALID_CREDENTIALS": InvalidCredentialsError,
        }.get(code, UnknownError)
        return error_class(*args, **kwargs)
    def to_safe_http_exception(self):
        return Err(
            HTTPException(
                status_code = self.status_code,
                detail      = self.detail
            )
        )

    def __str__(self):
        return f"{self.code} - [{self.status_code}]: {self._detail} (Raw: {self._raw_detail})"


class UnknownError(XError):
    def __init__(self,
        *args,
        detail:str="Unknown error occurred",
        raw_detail:Optional[str]=None,
        headers:Optional[dict]=None,
        metadata:Optional[Dict[str,Any]]={}
    ):
        super().__init__(detail=detail,headers=headers,raw_detail=raw_detail,metadata=metadata,*args)

    @property
    def status_code(self)->int:
        return 500

    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    
    @property
    def code(self) -> Optional[str]:
        return "X.UNKNOWN"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
    
class CreationError(XError):
    def __init__(self,
        *args,
        detail:str="Creation failed due to a conflict or invalid state",
        raw_detail:Optional[str]=None,
        headers:Optional[dict]=None,
        metadata:Optional[Dict[str,Any]]={}
    ):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    @property
    def status_code(self)->int:
        return 409
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error= self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.CREATION_ERROR"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
    

class AccessDenied(XError):
    def __init__(self,
        *args,
        detail:str="Access denied: insufficient permissions to perform the requested operation",
        raw_detail:Optional[str]=None,
        headers:Optional[dict]=None,
        metadata:Optional[Dict[str,Any]]={}
    ):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    @property
    def status_code(self)->int:
        return 401
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.ACCESS_DENIED"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers



class FailedToRemoveOwner(XError):
    def __init__(self, *args,
        detail:str="Failed to remove owner: resource must have at least one owner",
        raw_detail:Optional[str]=None,
        headers:Optional[dict]=None,
        metadata:Optional[Dict[str,Any]]={}
    ):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    
    @property
    def status_code(self)->int:
        return 409
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.FAILED_TO_REMOVE_OWNER"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers

class FailedToClaimResource(XError):
    def __init__(self,*args,
        detail:str="Failed to claim resource: resource is already claimed by another user",
        raw_detail:Optional[str]=None,
        headers:Optional[dict]=None,
        metadata:Optional[Dict[str,Any]]={}
    ):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)

    @property
    def status_code(self)->int:
        return 409
    
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.FAILED_TO_CLAIM_RESOURCE"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers


class TokenExpired(XError):
    def __init__(self, *args,detail:str="Token has expired",raw_detail:Optional[str]=None,headers:Optional[dict]=None,metadata:Optional[Dict[str,Any]]={}):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers)

    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.TOKEN_EXPIRED"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
    
    @property
    def status_code(self)->int:
        return 401

class LicenseCreationError(XError):
    def __init__(self, *args,detail:str="License creation failed due to a conflict or invalid state",raw_detail:Optional[str]=None,headers:Optional[dict]=None,metadata:Optional[Dict[str,Any]]={}):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.LICENSE_CREATION_ERROR"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def status_code(self)->int:
        return 409
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
   
class NotFound(XError):
    def __init__(self,*args,detail:str="Not found",raw_detail:Optional[str]=None,headers:Optional[dict]=None,metadata:Optional[Dict[str,Any]]={}):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.NOT_FOUND"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    
    @property
    def status_code(self)->int:
        return 404
    
    @property
    def headers(self) -> Optional[dict]:
        return self._headers


    
class AlreadyExists(XError):
    def __init__(self,*args,entity:str="Entity", id:str="",raw_detail:Optional[str]=None,headers:Optional[dict]=None,metadata:Optional[Dict[str,Any]]={}):
        detail = f"{entity.upper()} {id if id else ''} already exists."
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata={**metadata, "entity":entity,"id":id})

    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def status_code(self)->int:
        return 409
    
    @property
    def code(self) -> Optional[str]:
        return "X.ALREADY_EXISTS"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    
    @property
    def headers(self) -> Optional[dict]:
        return self._headers

class Unauthorized(XError):
    def __init__(self, *args,detail:str="Unauthorized: authentication is required and has failed or has not yet been provided",raw_detail:Optional[str]=None,headers:Optional[dict]=None,metadata:Optional[Dict[str,Any]]={}):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def code(self) -> Optional[str]:
        return "X.UNAUTHORIZED"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)

    @property
    def status_code(self)->int:
        return 401
    @property
    def headers(self) -> Optional[dict]:
        return self._headers

class UnauthorizedScope(XError):
    def __init__(self, *args,detail:str="Unauthorized scope: the provided token does not have the required scope for this operation",raw_detail:Optional[str]=None,headers:Optional[dict]=None,metadata:Optional[Dict[str,Any]]={}):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers,metadata=metadata)
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    
    @property
    def code(self) -> Optional[str]:
        return "X.UNAUTHORIZED_SCOPE"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)

    @property
    def status_code(self)->int:
        return 401
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
    
class InvalidLicense(XError):
    
    def __init__(self, *args,detail:str="Invalid license: the provided license is not valid or has expired",raw_detail:Optional[str]=None,headers:Optional[dict]=None):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers)
    
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    
    @property
    def status_code(self) -> int:
        """HTTP status code for the invalid license."""
        return 401  # or 403 if you prefer "Forbidden"
    @property
    def code(self) -> Optional[str]:
        return "X.INVALID_LICENSE"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers

    
class ServerError(XError):
    def __init__(self,*args,detail:str="Internal server error: an unexpected error occurred on the server",raw_detail:Optional[str]=None,headers:Optional[dict]=None):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers)
    
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )
    @property
    def status_code(self)->int:
        return 500
    @property
    def code(self) -> Optional[str]:
        return "X.SERVER_ERROR"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
    

class InvalidCredentialsError(XError):
    def __init__(self, *args,detail:str="Invalid credentials: the provided authentication credentials are incorrect",raw_detail:Optional[str]=None,headers:Optional[dict]=None):
        super().__init__(*args,detail=detail,raw_detail=raw_detail,headers=headers)
    
    @property
    def detail(self)->ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            detail      = self._detail,
            raw_error   = self.raw_detail
        )

    @property
    def status_code(self) -> int:
        """HTTP status code for invalid credentials."""
        return 401

    @property
    def code(self) -> Optional[str]:
        return "X.INVALID_CREDENTIALS"
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code,0)
    @property
    def headers(self) -> Optional[dict]:
        return self._headers
