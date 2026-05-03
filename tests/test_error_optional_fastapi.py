import builtins
import importlib.util
from pathlib import Path
import sys


def test_errors_module_works_without_fastapi():
    module_path = Path(__file__).resolve().parents[1] / "commonx" / "errors" / "__init__.py"
    spec = importlib.util.spec_from_file_location("commonx_errors_no_fastapi", module_path)
    module = importlib.util.module_from_spec(spec)
    original_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "fastapi":
            raise ModuleNotFoundError("fastapi intentionally unavailable for test")
        return original_import(name, *args, **kwargs)

    builtins.__import__ = blocked_import
    try:
        sys.modules.pop("commonx_errors_no_fastapi", None)
        spec.loader.exec_module(module)
    finally:
        builtins.__import__ = original_import
        sys.modules.pop("commonx_errors_no_fastapi", None)

    exc = module.AlreadyExists(metadata={"entity": "user", "id": "abc"}).to_http_exception()

    assert exc.status_code == 409
    assert exc.detail["code"] == "X.ALREADY_EXISTS"
    assert exc.detail["metadata"] == {"entity": "user", "id": "abc"}
