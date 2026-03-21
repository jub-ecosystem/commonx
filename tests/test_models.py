from commonx.models.mictlanx_api import UserProfileModel,XNode,NodeStatus,NodeType,StorageRef,Presentation
import pytest
from pydantic import ValidationError

def test_create_folder_success():
    """
    Test creating a basic folder (no storage ref needed).
    """
    folder = XNode(
        node_id="folder-photos",
        name="Photos",
        type=NodeType.FOLDER,
        owner_id="u_ignacio",
        status=NodeStatus.ACTIVE,
        parent_id=None
    )
    
    assert folder.node_id == "folder-photos"
    assert folder.name == "Photos"
    assert folder.is_folder is True
    assert folder.ancestors == []  # Default is empty list
    assert folder.storage is None  # Folders don't strictly need physical storage ref in this logic

    # Test various string inputs that should be sanitized to None
    for i in {"null","Null","NONE","undefined","nil",""}:
        folder2 = XNode(
            node_id="folder-2024",
            name="2024",
            type=NodeType.FOLDER,
            owner_id="u_ignacio",
            parent_id=i,
            ancestors=["folder-photos"]
        )
        assert folder2.parent_id is None
    # folder1 = XNode(
    #     node_id="folder-2023",
    #     name="2023",
    #     type=NodeType.FOLDER,
    #     owner_id="u_ignacio",
    #     parent_id="null",
    #     ancestors=["folder-photos"]
    # )


def test_create_file_success():
    """
    Test creating a file with a physical storage reference.
    """
    file_node = XNode(
        node_id   = "file-me-jpg",
        name      = "me.jpg",
        type      = NodeType.FILE,
        owner_id  = "u_ignacio",
        parent_id = "folder-photos",
        ancestors = ["folder-photos"],
        extension = "jpg",
        mime_type = "image/jpeg",
          # Nested Model
        storage=StorageRef(
            bucket_id  = "bucket-images-2026",
            ball_id    = "ball-xyz-123",
            size_bytes = 1024
        ),
          # Presentation
        presentation = Presentation(icon="mdi-image")
    )

    assert file_node.node_id == "file-me-jpg"
    assert file_node.is_folder is False
    assert file_node.storage.bucket_id == "bucket-images-2026"
    assert file_node.presentation.icon == "mdi-image"

# --- 2. VALIDATION FAILURES ---

def test_missing_required_fields():
    """
    Test that 'type' and 'name' are strictly required.
    """
    with pytest.raises(ValidationError) as exc:
        XNode(
            node_id="bad-node",
            owner_id="u_ignacio"
            # Missing name and type
        )
    
    errors = exc.value.errors()
    fields = [e["loc"][0] for e in errors]
    assert "name" in fields
    assert "type" in fields

def test_invalid_enum_status():
    """
    Test that we cannot assign a random string to 'status'.
    """
    with pytest.raises(ValidationError):
        XNode(
            node_id="bad-status",
            name="Test",
            type=NodeType.FILE,
            owner_id="u_ignacio",
            status="EXPLODED"  # Not in NodeStatus Enum
        )

# --- 3. LOGIC & DEFAULTS ---

def test_ancestors_default_list():
    """
    Ensure ancestors defaults to an empty list, not None.
    """
    node = XNode(
        node_id="node-1",
        name="Root",
        type=NodeType.FOLDER,
        owner_id="u_ignacio"
    )
    assert isinstance(node.ancestors, list)
    assert len(node.ancestors) == 0



def test_presentation_customization():
    """
    Verify the UI presentation layer accepts custom values.
    """
    folder = XNode(
        node_id="folder-red",
        name="Urgent",
        type=NodeType.FOLDER,
        owner_id="u_1",
        presentation=Presentation(
            color="#FF0000",
            view_mode="list"
        )
    )
    
    assert folder.presentation.color == "#FF0000"
    assert folder.presentation.view_mode == "list"

def test_user_profile_model_defaults():
    user_profile = UserProfileModel(
        user_id    = "user123",
    ).from_name(name="John Doe")

    print(user_profile)
    assert user_profile.user_id == "user123"
    assert user_profile.bio == ""
    assert user_profile.language == "en"
    # assert user_profile.color == "blue"
    assert user_profile.local_path is None
    assert user_profile.created_at is not None
    assert user_profile.updated_at is not None