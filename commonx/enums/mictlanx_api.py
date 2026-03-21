from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class NodeType(str, Enum):
    FOLDER = "FOLDER"
    FILE   = "FILE"

class NodeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    TRASHED = "TRASHED"      # In the Recycle Bin
    DELETED = "DELETED"      # Purged forever
    UPLOADING = "UPLOADING"  # File is reserving space but not ready yet