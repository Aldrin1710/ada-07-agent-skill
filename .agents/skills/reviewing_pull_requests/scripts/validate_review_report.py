#!/usr/bin/env python3
"""Valida la estructura (no la calidad) de un reporte de revisión de PR.

Uso:
    python validate_review_report.py results/pr-readiness-review.md

Código de salida:
    0  -> el formato es válido.
    1  -> falta una sección o línea obligatoria.
    2  -> el archivo no existe o no se pudo leer.
"""
import re
import sys

REQUIRED_HEADINGS = [
    "Review Context",
    "Requirements / Acceptance Criteria Reviewed",
    "Test Evidence",
    "MUST FIX",
    "SHOULD FIX",
    "OPTIONAL",
    "Final Review Summary",
]
REQUIRED_LINES = [
    "Human decision required",
]


def has_heading(text: str, title: str) -> bool:
    pattern = r"^\s{0,3}#{1,6}\s+" + re.escape(title) + r"\s*$"
    return re.search(pattern, text, re.MULTILINE | re.IGNORECASE) is not None


def has_line(text: str, label: str) -> bool:
    pattern = r"^\s*" + re.escape(label) + r"\s*:"
    return re.search(pattern, text, re.MULTILINE | re.IGNORECASE) is not None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Uso: validate_review_report.py <ruta-al-reporte.md>")
        return 2

    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        print(f"INVALID: no se pudo leer el archivo '{path}': {exc}")
        return 2

    missing = [f"sección '{h}'" for h in REQUIRED_HEADINGS if not has_heading(text, h)]
    missing += [f"línea '{l}:'" for l in REQUIRED_LINES if not has_line(text, l)]

    if missing:
        print("INVALID: falta contenido obligatorio en el reporte:")
        for item in missing:
            print(f"  - {item}")
        print("exit code: 1")
        return 1

    print("VALID: PR readiness review structure is complete.")
    print("exit code: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
