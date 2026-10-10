"""Workspace-contained input path validation for the composite Action."""
from __future__ import annotations

from pathlib import Path


def resolve_workspace_path(
    workspace: Path, raw_path: str, *, label: str, require_file: bool = False
) -> Path:
    """Resolve one existing input path without allowing it to escape the checkout."""
    raw_path = raw_path.strip()
    if not raw_path:
        raise ValueError(f"{label} must not be empty")
    root = workspace.resolve()
    candidate = Path(raw_path)
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError(f"{label} must stay inside GITHUB_WORKSPACE") from None
    if not resolved.exists():
        raise ValueError(f"{label} does not exist")
    if require_file and not resolved.is_file():
        raise ValueError(f"{label} must be a file")
    return resolved
