"""
Skrypt automatycznie generujący diagramy klas dla modułów Python i Scala.

Co robi:
  1. Skanuje src/python/ — generuje PNG dla każdego pliku z klasami przez pyreverse
  2. Uruchamia sbt classDiagram — generuje PNG hierarchii klas Scali przez Graphviz
  3. Tworzy pliki .md dla każdego diagramu w docs/diagrams/
  4. Aktualizuje sekcje nav w mkdocs.yml

Wymagania:
  pip install pylint     (dostarcza pyreverse)
  apt install graphviz   (wymagany przez pyreverse i sbt-class-diagram)
  sbt plugin: sbt-class-diagram (skonfigurowany w project/plugins.sbt)

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
DOCS_DIAGRAMS_SCALA = DOCS_DIAGRAMS / "scala"
MKDOCS_YML = ROOT / "mkdocs.yml"

DOCS_DIAGRAMS.mkdir(parents=True, exist_ok=True)
DOCS_DIAGRAMS_SCALA.mkdir(parents=True, exist_ok=True)


# ── Python ────────────────────────────────────────────────────────────────────

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
    """Generuje PNG dla pliku Python przez pyreverse."""
    module_name = py_file.stem
    project_name = f"py_{module_name}"
    output_png = DOCS_DIAGRAMS / f"classes_{project_name}.png"

    result = subprocess.run(
        ["pyreverse", "-o", "png", "-p", project_name, "--colorized", str(py_file)],
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

    print(f"  [Python] BŁĄD dla {py_file.name}: {result.stderr.strip()[:200]}")
    return None


def create_python_diagram_md(py_file: Path, png_path: Path) -> Path:
    """Tworzy stronę dokumentacji z diagramem dla modułu Python."""
    module_name = py_file.stem
    md_path = DOCS_DIAGRAMS / f"python_{module_name}.md"
    content = f"# {module_name}\n\n![Diagram klas {module_name}]({png_path.name})\n"
    md_path.write_text(content, encoding="utf-8")
    return md_path


# ── Scala ─────────────────────────────────────────────────────────────────────

def generate_scala_diagrams() -> list[Path]:
    """
    Uruchamia sbt classDiagram i kopiuje wygenerowane PNG do docs/diagrams/scala/.

    sbt-class-diagram generuje plik diagram.png w target/ dla każdego pakietu.
    Wymaga: enablePlugins(ClassDiagramPlugin) w build.sbt oraz Graphviz.

    Returns:
        Lista skopiowanych plików PNG.
    """
    print("  [Scala]  Uruchamianie sbt classDiagram...")

    result = subprocess.run(
        ["sbt", "classDiagram"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    if result.returncode != 0:
        print(f"  [Scala]  BŁĄD sbt classDiagram:\n    {result.stderr.strip()[:300]}")
        return []

    # sbt-class-diagram zapisuje wynik do target/scala-*/classes_diagram.png lub podobnie
    pngs = list((ROOT / "target").rglob("*diagram*.png"))
    # Pomiń małe ikonki nawigacyjne Scaladoc (< 2 KB)
    pngs = [p for p in pngs if p.stat().st_size > 2048]

    copied: list[Path] = []
    for png in sorted(pngs):
        dest = DOCS_DIAGRAMS_SCALA / png.name
        shutil.copy2(str(png), str(dest))
        copied.append(dest)
        print(f"  [Scala]  OK: {png.name}")

    return copied


def create_scala_diagram_md(png_files: list[Path]) -> Path | None:
    """Tworzy stronę dokumentacji z diagramami Scala. Zwraca None jeśli brak PNG."""
    if not png_files:
        return None

    md_path = DOCS_DIAGRAMS / "scala_diagrams.md"
    lines = ["# Diagramy klas: Scala\n"]
    for png in png_files:
        title = png.stem.replace("_", " ").replace("-", " ").title()
        lines.append(f"## {title}\n")
        lines.append(f"![{title}](scala/{png.name})\n")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


# ── mkdocs.yml nav ────────────────────────────────────────────────────────────

def update_mkdocs_nav(
    python_mds: list[tuple[str, Path]],
    scala_md: Path | None,
) -> None:
    """Nadpisuje sekcje Diagramów w nav mkdocs.yml."""
    content = MKDOCS_YML.read_text(encoding="utf-8")

    # Usuń stare sekcje
    content = re.sub(r"\n    - Diagramy Python:.*?(?=\n    - |\Z)", "", content, flags=re.DOTALL)
    content = re.sub(r"\n    - Diagramy Scala:.*?(?=\n    - |\Z)", "", content, flags=re.DOTALL)

    new_entries: list[str] = []

    if python_mds:
        new_entries.append("    - Diagramy Python:")
        for name, md_path in sorted(python_mds):
            rel = md_path.relative_to(ROOT / "docs")
            new_entries.append(f"          - {name}: {rel}")

    if scala_md:
        new_entries.append("    - Diagramy Scala:")
        rel = scala_md.relative_to(ROOT / "docs")
        new_entries.append(f"          - Wszystkie diagramy: {rel}")

    if not new_entries:
        print("  [nav]    Brak diagramów — nav bez zmian")
        return

    insert = "\n".join(new_entries) + "\n"
    content = content.replace(
        "    - Moduł Scali (API):",
        f"{insert}    - Moduł Scali (API):",
    )

    MKDOCS_YML.write_text(content, encoding="utf-8")
    print("  [nav]    Zaktualizowano mkdocs.yml")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=== Generowanie diagramów ===\n")

    print("-- Python --")
    python_mds: list[tuple[str, Path]] = []
    for py_file in get_python_modules():
        png = generate_python_diagram(py_file)
        if png:
            md = create_python_diagram_md(py_file, png)
            python_mds.append((py_file.stem, md))

    print("\n-- Scala --")
    scala_pngs = generate_scala_diagrams()
    scala_md = create_scala_diagram_md(scala_pngs)
    if not scala_pngs:
        print("  [Scala]  Brak diagramów — sekcja Scala pominięta w nav")

    print("\n-- mkdocs.yml --")
    update_mkdocs_nav(python_mds, scala_md)

    print("\n=== Gotowe ===")


if __name__ == "__main__":
    main()
