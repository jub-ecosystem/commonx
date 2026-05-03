# Copilot Instructions

## Build, test, and lint

- Install dependencies: `poetry install`
- Build the package: `poetry build`
- Run the full test suite the same way CI does: `poetry run coverage run -m pytest -v -s && poetry run coverage report -m`
- Run one test file: `poetry run pytest tests/test_models.py -v -s`
- Run one test: `poetry run pytest tests/test_models.py::test_create_folder_success -v -s`
- Lint: `python -m pip install ruff && python -m ruff check .`  
  CI installs Ruff ad hoc and runs `ruff check .`; Ruff is not listed in `pyproject.toml`.

## High-level architecture

`commonx` is an internal shared package for Jub services. The code is organized around reusable Pydantic types rather than application entrypoints.

- `commonx/models/` holds shared domain models. Most of them inherit `TimestampMixin`, which adds UTC `created_at` and `updated_at` fields automatically.
- `commonx/dto/` holds request/response payload models used by other services. There are two main namespaces: `xolo` for auth, users, groups, scopes, licenses, and permissions; and `mictlanx_api` for file-tree and profile payloads.
- `commonx/enums/` defines the enum types consumed by both models and DTOs, especially access-control enums in `xolo` and file-node enums in `mictlanx_api`.
- `commonx/errors/` centralizes the shared error taxonomy. `XError` subclasses carry HTTP status, stable string codes, integer code mappings, optional metadata, and helpers to convert into FastAPI `HTTPException`s.

The most connected flow spans `enums -> models -> dto -> tests`: enum values constrain model fields, models add validators/default behavior, DTOs sometimes derive presentation fields from validated data, and tests mostly lock down validation and defaulting behavior rather than service logic.

## Key conventions

- Shared models and DTOs almost always set `model_config = ConfigDict(str_strip_whitespace=True)`. Keep that on new string-heavy Pydantic types so whitespace trimming stays consistent across packages.
- When a model represents persisted/shared domain data, inherit from `TimestampMixin` instead of redefining timestamps.
- Normalize nullable identifier fields with validators that call `Helpers.sanitize_null_id_none(...)`. In this repo, values like `""`, `"null"`, `"none"`, `"undefined"`, and `"nil"` are treated as `None`.
- Derived fields are often populated inside model logic instead of by callers. Examples: `User` generates a default `profile_photo`, `UserProfileModel.from_name()` fills avatar/color data, and `FileXNodeDTO` computes `size_str` from `size_bytes`.
- Error handling is built around typed `XError` subclasses plus `XError.from_code(...)`. When creating new shared errors, keep them in `commonx/errors/__init__.py`, assign a stable `X.*` code, add the integer mapping in `ERROR_CODES`, and preserve metadata-driven messages like `AlreadyExists` and `NotFound`.
- Tests are organized around model behavior and validation edges. Add or update tests in `tests/` when changing defaults, validators, enum constraints, or generated fields.
