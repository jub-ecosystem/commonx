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
    msg: str
    raw_error: Optional[str] = None
    metadata: Optional[Dict[str,Any]] = None
    
    def __init__(self, **data):
        if data.get('metadata') is None:
            data['metadata'] = {}
        super().__init__(**data)



class XError(Exception,ABC):
    """
    XError
    An abstract base exception class for handling custom application errors with structured error information.
    This class provides a framework for creating custom exceptions with standardized error handling,
    including HTTP status codes, error codes, metadata, and detailed error information.
    Attributes:
        msg (str): Human-readable error message.
        _headers (dict): HTTP headers to include in responses. Defaults to empty dict.
        _raw_detail (Optional[str]): Raw error detail information from the underlying exception.
        metadata (dict): Additional metadata associated with the error. Defaults to empty dict.
    Abstract Properties:
        status_code (int): HTTP status code for the error. Must be implemented by subclasses.
        code (Optional[str]): Error code identifier. Must be implemented by subclasses.
        code_int (Optional[int]): Integer representation of the error code. Must be implemented by subclasses.
    Properties:
        detail (ErrorDetail): Structured error detail object containing HTTP status, code, message, and metadata.
        raw_detail (Optional[str]): Returns the raw error detail string.
        headers (Optional[dict]): Returns HTTP headers associated with the error.
    Methods:
        to_http_exception() -> HTTPException: Converts the error to an HTTPException for HTTP responses.
        to_safe_http_exception() -> Err: Safely converts the error to an HTTPException wrapped in an Err result.
        from_exception(exc: Exception) -> XError: Static method to create an XError from a generic exception.
        from_exception_safe(exc: Exception) -> XError: Static method to safely create an XError from a generic exception, wrapped in an Err result.
        from_code_safe(code: str, *args, **kwargs) -> XError: Static method to create an XError by code string, wrapped in an Err result.
        from_code(code: str, *args, **kwargs) -> XError: Static method to create an XError by code string.
        __str__() -> str: Returns a formatted string representation of the error including code, status, message, and raw details.
    """
    def __init__(self, *args, msg:str, raw_detail:Optional[str]=None, headers:Optional[dict]=None, metadata:Optional[Dict[str,Any]]=None):
        super().__init__(*args)
        self.msg = msg
        self._headers = headers if headers is not None else {}
        self._raw_detail = raw_detail
        self.metadata = metadata if metadata is not None else {}
    
    @property
    @abstractmethod
    def status_code(self)->int:
        pass
    
    @property
    def detail(self) -> ErrorDetail:
        return ErrorDetail(
            http_status = self.status_code,
            code        = self.code,
            code_int    = ERROR_CODES.get(self.code, -1),
            msg         = self.msg,
            raw_error   = self.raw_detail,
            metadata    = self.metadata
        )
    
    @property
    def raw_detail(self) -> Optional[str]:
        return self._raw_detail
    
    @property
    @abstractmethod
    def code(self) -> Optional[str]:
        pass
    
    @property
    @abstractmethod
    def code_int(self) -> Optional[int]:
        pass
    
    @property
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
    def from_exception_safe( exc: Exception):
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
        print("KWARGS:", kwargs)
        return error_class(*args, **kwargs)
    def to_safe_http_exception(self):
        return Err(
            HTTPException(
                status_code = self.status_code,
                detail      = self.detail
            )
        )

    def __str__(self):
        return f"{self.code} - [{self.status_code}]: {self.msg} (Raw: {self._raw_detail})"


class UnknownError(XError):
    def __init__(self, *args, msg: str = "Unknown error occurred", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def status_code(self) -> int:
        return 500
    
    @property
    def code(self) -> Optional[str]:
        return "X.UNKNOWN"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class CreationError(XError):
    def __init__(self, *args, msg: str = "Creation failed due to a conflict or invalid state", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def status_code(self) -> int:
        return 409

    @property
    def code(self) -> Optional[str]:
        return "X.CREATION_ERROR"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class AccessDenied(XError):
    def __init__(self, *args, msg: str = "Access denied: insufficient permissions to perform the requested operation", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def status_code(self) -> int:
        return 401

    @property
    def code(self) -> Optional[str]:
        return "X.ACCESS_DENIED"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class FailedToRemoveOwner(XError):
    def __init__(self, *args, msg: str = "Failed to remove owner: resource must have at least one owner", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)
    
    @property
    def status_code(self) -> int:
        return 409

    @property
    def code(self) -> Optional[str]:
        return "X.FAILED_TO_REMOVE_OWNER"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class FailedToClaimResource(XError):
    def __init__(self, *args, msg: str = "Failed to claim resource: resource is already claimed by another user", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def status_code(self) -> int:
        return 409
    
    @property
    def code(self) -> Optional[str]:
        return "X.FAILED_TO_CLAIM_RESOURCE"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class TokenExpired(XError):
    def __init__(self, *args, msg: str = "Token has expired", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def code(self) -> Optional[str]:
        return "X.TOKEN_EXPIRED"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)
    
    @property
    def status_code(self) -> int:
        return 401


class LicenseCreationError(XError):
    def __init__(self, *args, msg: str = "License creation failed due to a conflict or invalid state", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def code(self) -> Optional[str]:
        return "X.LICENSE_CREATION_ERROR"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)

    @property
    def status_code(self) -> int:
        return 409


class NotFound(XError):
    def __init__(self, *args, msg: str = "Not found", **kwargs):
        metadata = kwargs.get("metadata", {})
        entity = metadata.get("entity", "RESOURCE")
        id = metadata.get("id", None)
        msg = msg if msg is not None else f"<{entity.upper()}> {id if id else ''} not found."
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def code(self) -> Optional[str]:
        return "X.NOT_FOUND"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)
    
    @property
    def status_code(self) -> int:
        return 404


class AlreadyExists(XError):
    def __init__(self, *args, msg: str = None, **kwargs):
        metadata = kwargs.get("metadata", {})
        entity = metadata.get("entity", "RESOURCE")
        id = metadata.get("id", None)
        msg = msg if msg is not None else f"<{entity.upper()}> {id if id else ''} already exists."
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def status_code(self) -> int:
        return 409
    
    @property
    def code(self) -> Optional[str]:
        return "X.ALREADY_EXISTS"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class Unauthorized(XError):
    def __init__(self, *args, msg: str = "Unauthorized: authentication is required and has failed or has not yet been provided", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)
    
    @property
    def code(self) -> Optional[str]:
        return "X.UNAUTHORIZED"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)

    @property
    def status_code(self) -> int:
        return 401


class UnauthorizedScope(XError):
    def __init__(self, *args, msg: str = "Unauthorized scope: the provided token does not have the required scope for this operation", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)
    
    @property
    def code(self) -> Optional[str]:
        return "X.UNAUTHORIZED_SCOPE"
    
    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)

    @property
    def status_code(self) -> int:
        return 401


class InvalidLicense(XError):
    def __init__(self, *args, msg: str = "Invalid license: the provided license is not valid or has expired", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)
    
    @property
    def status_code(self) -> int:
        return 401

    @property
    def code(self) -> Optional[str]:
        return "X.INVALID_LICENSE"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class ServerError(XError):
    def __init__(self, *args, msg: str = "Internal server error: an unexpected error occurred on the server", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)
    
    @property
    def status_code(self) -> int:
        return 500

    @property
    def code(self) -> Optional[str]:
        return "X.SERVER_ERROR"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)


class InvalidCredentialsError(XError):
    def __init__(self, *args, msg: str = "Invalid credentials: the provided authentication credentials are incorrect", **kwargs):
        super().__init__(*args, msg=msg, **kwargs)

    @property
    def status_code(self) -> int:
        return 401

    @property
    def code(self) -> Optional[str]:
        return "X.INVALID_CREDENTIALS"

    @property
    def code_int(self) -> Optional[int]:
        return ERROR_CODES.get(self.code, 0)
