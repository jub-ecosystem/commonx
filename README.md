# Commonx

[![Version](https://img.shields.io/github/v/tag/jub-ecosystem/commonx?label=version)](https://github.com/jub-ecosystem/commonx/tags)
[![Tests](https://github.com/jub-ecosystem/commonx/actions/workflows/run_test.yml/badge.svg)](https://github.com/jub-ecosystem/commonx/actions/workflows/run_test.yml)
[![codecov](https://codecov.io/gh/jub-ecosystem/commonx/branch/master/graph/badge.svg)](https://codecov.io/gh/jub-ecosystem/commonx)

`commonx` is the shared Python library for the Jub ecosystem. Its purpose is to keep common contracts and behaviors in one place so multiple services can speak the same language without duplicating models, enums, validation rules, or error handling.

This package is mainly useful when different apps need to exchange the same payloads or follow the same domain rules. Instead of redefining user schemas, file node models, permission enums, or structured errors in each service, they can import the shared definitions from `commonx`.

## What this library provides

- `commonx.dto`: shared request/response DTOs for auth, users, groups, scopes, licenses, and file-tree related payloads.
- `commonx.models`: reusable domain models with validation and shared timestamp behavior.
- `commonx.enums`: enum definitions used across the DTOs and models.
- `commonx.errors`: a structured error system with stable error codes and helpers for HTTP-style error responses.
- `commonx.helpers`: small reusable helpers used by shared models.

## Why it exists

The main goal of this library is consistency across services:

- one definition for common payloads
- one place for shared enum values
- one error taxonomy shared by APIs
- one source of validation logic for reusable models

That makes service-to-service integration simpler and reduces drift between repositories.

## Installation

Base install:

```bash
pip install commonx
```

Optional FastAPI integration for `commonx.errors`:

```bash
pip install "commonx[fastapi]"
```

## Example usage

```python
from commonx.models.mictlanx_api import XNode
from commonx.enums.mictlanx_api import NodeType
from commonx.errors import AlreadyExists

node = XNode(
    node_id="folder-photos",
    name="Photos",
    type=NodeType.FOLDER,
    owner_id="user-123",
)

error = AlreadyExists(metadata={"entity": "user", "id": "john"})
```

## Notes

- This is an internal shared library for Jub projects.
- FastAPI is optional; only the error helpers need HTTPException-compatible behavior.
