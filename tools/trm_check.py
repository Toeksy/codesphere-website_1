#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRM Check – Lightweight consistency checks for CI/hooks.

Checks:
- `trm/state.json` exists and is `idle` (no active session)
- `trm/memory.md` exists and contains the insertion marker

Exit codes:
- 0 = OK
- 1 = Failed checks
- 2 = Unexpected error
"""

from __future__ import annotations

import json
from pathlib import Path


MARKER = "## (Lisää tulevat sessionit tänne)"


def fail(message: str) -> int:
    print(f"❌ TRM check failed: {message}")
    return 1


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    trm_dir = repo_root / "trm"
    state_file = trm_dir / "state.json"
    memory_file = trm_dir / "memory.md"

    if not state_file.exists():
        return fail(f"Missing {state_file}")

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"Invalid JSON in {state_file}: {exc}")

    status = state.get("status")
    task = state.get("task", "")

    if status != "idle":
        return fail(
            f"Active TRM session detected (status={status!r}, task={task!r}). "
            "Finalize/reset before committing/merging."
        )

    if not memory_file.exists():
        return fail(f"Missing {memory_file}")

    try:
        memory_text = memory_file.read_text(encoding="utf-8")
    except Exception as exc:
        return fail(f"Cannot read {memory_file}: {exc}")

    if MARKER not in memory_text:
        return fail(
            f"Missing marker in {memory_file}: {MARKER!r}. "
            "Finalize script expects this marker for insertion."
        )

    print("✅ TRM check OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"❌ TRM check crashed: {exc}")
        raise SystemExit(2)
