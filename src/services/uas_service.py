"""Audit kelengkapan file, kerangka, dan artefak; bukan sertifikasi nilai UAS."""
from __future__ import annotations

import ast
from pathlib import Path

from src.uas import SESSIONS

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ("visual", "screenshot", "table", "benchmark", "slides", "interpretation")


def session_checklist(root: Path = ROOT) -> list[dict]:
    rows = []
    for spec in SESSIONS:
        missing, todos, parse_errors = [], 0, []
        for name in spec.files:
            path = root / name
            if not path.is_file():
                missing.append(name)
                continue
            # Hitung raise nyata, bukan kata TODO dalam dokumentasi.
            try:
                tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            except (SyntaxError, UnicodeError) as exc:
                parse_errors.append(f"{name}: {exc}")
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Raise):
                    exc = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
                    todos += isinstance(exc, ast.Name) and exc.id == "NotImplementedError"
        evidence_dir = root / "docs" / "evidence" / spec.code
        artifacts = {}
        for category in ARTIFACTS:
            folder = evidence_dir / category
            artifacts[category] = sum(
                p.is_file() and p.stat().st_size > 0 and p.name != ".gitkeep"
                for p in folder.rglob("*")
            ) if folder.is_dir() else 0
        rows.append({
            "Sesi": spec.code, "Topik": spec.title, "Bobot": spec.weight,
            "Pemilik": spec.owner, "Kolaborator": spec.collaborators or "—",
            "Reviewer": spec.reviewer,
            "Kode": "Error sintaks/encoding" if parse_errors else "File belum tersedia" if missing
                    else "Kerangka / TODO" if todos else "Perlu uji lengkap",
            "Error": "\n".join(parse_errors),
            "TODO": todos, "File belum ada": ", ".join(missing),
            "File tes tersedia": sum((root / p).is_file() for p in spec.tests),
            "File tes direncanakan": len(spec.tests),
            **artifacts,
        })
    return rows
