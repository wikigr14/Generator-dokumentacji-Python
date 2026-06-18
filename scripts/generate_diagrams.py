"""
Skrypt automatycznie generujący diagramy klas dla wszystkich modułów Python.

Co robi:
  1. Skanuje src/python/ w poszukiwaniu plików .py
  2. Dla każdego pliku generuje PNG przez pyreverse
  3. Tworzy plik .md dla każdego diagramu w docs/diagrams/
  4. Aktualizuje sekcję "Diagramy Python" w nav mkdocs.yml

Uwaga dotycząca Scali:
  sbt doc -diagrams generuje diagramy jako interaktywne elementy HTML
  wbudowane w Scaladoc — nie jako osobne pliki PNG do osadzenia.
  Pełna dokumentacja Scali dostępna jest przez iframe w sekcji "Moduł Scali (API)".

Użycie:
  python scripts/generate_diagrams.py
"""

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC_PYTHON = ROOT / "src" / "python"
DOCS_DIAGRAMS = ROOT / "docs" / "diagrams"
MKDOCS_YML = ROOT / "mkdocs.yml"

DOCS_DIAGRAMS.mkdir(parents=True, exist_ok=True)


def has_classes(py_file: Path) -> bool:
    """Zwraca True jeśli plik .py zawiera definicje klas."""
    content = py_file.read_text(encoding="utf-8")
    return bool(re.search(r"^\s*class\s+\w+", content, re.MULTILINE))


def get_python_modules() -> list[Path]:
    """Zwraca posortowaną listę plików .py z src/python/ które zawierają klasy."""
    return sorted(
        f for f in SRC_PYTHON.glob("*.py")
        if f.name != "__init__.py"
        and not f.name.startswith(".")
        and has_classes(f)
    )


def generate_python_diagram(py_file: Path) -> Path | None:
    """
    Generuje diagram klas PNG dla pliku Python przez pyreverse.

    Args:
        py_file: Ścieżka do pliku .py.

    Returns:
        Ścieżka do wygenerowanego PNG lub None jeśli generowanie się nie powiodło.
    """
    module_name = py_file.stem
    project_name = f"py_{module_name}"
    output_png = DOCS_DIAGRAMS / f"classes_{project_name}.png"

    result = subprocess.run(
        [
            "pyreverse",
            "-o", "png",
            "-p", project_name,
            "--colorized",        # kolorowe klasy wg typu (klasa/interfejs/abstrakcyjna)
            "--max-color-depth=3",
            str(py_file),
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    generated = ROOT / f"classes_{project_name}.png"
    packages = ROOT / f"packages_{project_name}.png"

    if packages.exists():
        packages.unlink()

    if generated.exists():
        shutil.move(str(generated), str(output_png))
        print(f"  [Python] OK: {output_png.name}")
        return output_png

    print(f"  [Python] BŁĄD dla {py_file.name}:\n    {result.stderr.strip()}")
    return None


def create_python_diagram_md(py_file: Path, png_path: Path) -> Path:
    """
    Tworzy stronę dokumentacji z diagramem dla modułu Python.

    Args:
        py_file: Plik źródłowy .py.
        png_path: Wygenerowany PNG.

    Returns:
        Ścieżka do pliku .md.
    """
    module_name = py_file.stem
    md_path = DOCS_DIAGRAMS / f"python_{module_name}.md"

    content = (
        f"# {module_name}\n\n"
        f"![Diagram klas {module_name}]({png_path.name})\n"
    )
    md_path.write_text(content, encoding="utf-8")
    return md_path


def update_mkdocs_nav(python_mds: list[tuple[str, Path]]) -> None:
    """
    Nadpisuje sekcję 'Diagramy Python' w nav mkdocs.yml.
    Pozostałe sekcje pozostają bez zmian.

    Args:
        python_mds: Lista (nazwa_modułu, ścieżka_md).
    """
    if not python_mds:
        print("  [nav]    Brak diagramów — nav bez zmian")
        return

    content = MKDOCS_YML.read_text(encoding="utf-8")

    # Usuń starą sekcję Diagramy Python jeśli istnieje
    content = re.sub(
        r"\n    - Diagramy Python:.*?(?=\n    - |\Z)",
        "",
        content,
        flags=re.DOTALL,
    )

    # Zbuduj nowe wpisy
    lines = ["    - Diagramy Python:"]
    for name, md_path in sorted(python_mds):
        rel = md_path.relative_to(ROOT / "docs")
        lines.append(f"          - {name}: {rel}")
    insert = "\n".join(lines) + "\n"

    # Wstaw przed "Moduł Scali (API)"
    content = content.replace(
        "    - Moduł Scali (API):",
        f"{insert}    - Moduł Scali (API):",
    )

    MKDOCS_YML.write_text(content, encoding="utf-8")
    print("  [nav]    Zaktualizowano mkdocs.yml")


def main() -> None:
    print("=== Generowanie diagramów ===\n")

    python_mds: list[tuple[str, Path]] = []
    for py_file in get_python_modules():
        png = generate_python_diagram(py_file)
        if png:
            md = create_python_diagram_md(py_file, png)
            python_mds.append((py_file.stem, md))

    print()
    update_mkdocs_nav(python_mds)
    print("\n=== Gotowe ===")


if __name__ == "__main__":
    main()
