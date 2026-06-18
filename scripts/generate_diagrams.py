"""
Skrypt automatycznie generujący diagramy klas dla wszystkich modułów Python i Scala.

Co robi:
  1. Skanuje src/python/ i src/main/scala/ w poszukiwaniu plików źródłowych
  2. Dla każdego pliku/pakietu Pythona generuje PNG przez pyreverse
  3. Dla Scali kopiuje grafy wygenerowane przez sbt doc (-diagrams)
  4. Tworzy plik .md dla każdego diagramu w docs/diagrams/
  5. Aktualizuje sekcję nav w mkdocs.yml — dodaje sekcje "Diagramy Python" i "Diagramy Scala"

Użycie:
  python scripts/generate_diagrams.py
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

# ── Ścieżki projektu ──────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
SRC_PYTHON = ROOT / "src" / "python"
SRC_SCALA = ROOT / "src" / "main" / "scala"
DOCS_DIAGRAMS = ROOT / "docs" / "diagrams"
MKDOCS_YML = ROOT / "mkdocs.yml"

DOCS_DIAGRAMS.mkdir(parents=True, exist_ok=True)


# ── Python: generowanie PNG przez pyreverse ───────────────────────────────────

def get_python_modules() -> list[Path]:
    """Zwraca listę plików .py z src/python/ (pomija __init__.py i .gitkeep)."""
    return [
        f for f in SRC_PYTHON.glob("*.py")
        if f.name not in ("__init__.py",) and not f.name.startswith(".")
    ]


def generate_python_diagram(py_file: Path) -> Path | None:
    """
    Generuje diagram klas PNG dla pojedynczego pliku Python.

    Args:
        py_file: Ścieżka do pliku .py.

    Returns:
        Ścieżka do wygenerowanego PNG lub None jeśli generowanie się nie powiodło.
    """
    module_name = py_file.stem
    project_name = f"py_{module_name}"
    output_png = DOCS_DIAGRAMS / f"classes_{project_name}.png"

    result = subprocess.run(
        ["pyreverse", "-o", "png", "-p", project_name, str(py_file)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    generated = ROOT / f"classes_{project_name}.png"
    packages = ROOT / f"packages_{project_name}.png"

    if generated.exists():
        shutil.move(str(generated), str(output_png))
        if packages.exists():
            packages.unlink()
        print(f"  [Python] Wygenerowano: {output_png.name}")
        return output_png
    else:
        print(f"  [Python] BŁĄD dla {py_file.name}: {result.stderr.strip()}")
        return None


# ── Scala: kopiowanie grafów z Scaladoc (-diagrams) ───────────────────────────

def get_scaladoc_diagrams() -> list[Path]:
    """
    Szuka PNG wygenerowanych przez sbt doc -diagrams w target/scala-*/api/.
    Graphviz generuje pliki *.png zawierające 'diagram' w nazwie lub ścieżce.

    Returns:
        Lista ścieżek do PNG z Scaladoc.
    """
    api_dirs = list((ROOT / "target").glob("scala-*/api"))
    diagrams = []
    for api_dir in api_dirs:
        diagrams.extend(api_dir.rglob("*.png"))
    return diagrams


def copy_scala_diagrams() -> list[Path]:
    """
    Kopiuje diagramy Scala z Scaladoc do docs/diagrams/.

    Returns:
        Lista skopiowanych plików PNG.
    """
    scala_diagrams_dir = DOCS_DIAGRAMS / "scala"
    scala_diagrams_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for png in get_scaladoc_diagrams():
        # Nazwa: zachowaj strukturę pakietów jako prefix
        dest_name = png.name
        dest = scala_diagrams_dir / dest_name
        shutil.copy2(str(png), str(dest))
        copied.append(dest)
        print(f"  [Scala]  Skopiowano: {dest.relative_to(DOCS_DIAGRAMS)}")

    return copied


# ── Generowanie plików .md ─────────────────────────────────────────────────────

def create_python_md(py_file: Path, png_path: Path) -> Path:
    """
    Tworzy plik .md dla diagramu modułu Python.

    Args:
        py_file: Plik źródłowy .py.
        png_path: Wygenerowany PNG.

    Returns:
        Ścieżka do utworzonego pliku .md.
    """
    module_name = py_file.stem
    md_path = DOCS_DIAGRAMS / f"python_{module_name}.md"
    rel_png = png_path.name  # PNG jest w tym samym folderze docs/diagrams/

    content = f"""# Diagram klas: `{module_name}.py`

Wygenerowany automatycznie przez `pyreverse` z pliku `src/python/{py_file.name}`.

![Diagram klas {module_name}]({rel_png})

!!! info "Szczegółowa dokumentacja API"
    Pełna dokumentacja metod i klas dostępna jest w sekcji
    [Moduł Pythona](../python.md).
"""
    md_path.write_text(content, encoding="utf-8")
    return md_path


def create_scala_md(png_files: list[Path]) -> Path:
    """
    Tworzy zbiorczy plik .md z wszystkimi diagramami Scala.

    Args:
        png_files: Lista PNG wygenerowanych przez Scaladoc.

    Returns:
        Ścieżka do utworzonego pliku .md.
    """
    md_path = DOCS_DIAGRAMS / "scala_diagrams.md"

    if not png_files:
        content = """# Diagramy klas: Scala

!!! warning "Diagramy niedostępne"
    Diagramy Scaladoc są generowane przez `sbt doc` z flagą `-diagrams`
    w środowisku CI/CD. Lokalnie uruchom `sbt doc` po instalacji Graphviz.
"""
    else:
        sections = []
        for png in sorted(png_files):
            # Nazwa pliku jako tytuł sekcji
            title = png.stem.replace("_", " ").replace(".", " ")
            rel_png = f"scala/{png.name}"
            sections.append(f"## {title}\n\n![{title}]({rel_png})\n")

        content = "# Diagramy klas: Scala\n\n"
        content += "Wygenerowane automatycznie przez `sbt doc -diagrams` z kodu źródłowego.\n\n"
        content += "\n".join(sections)

    md_path.write_text(content, encoding="utf-8")
    return md_path


# ── Aktualizacja mkdocs.yml ────────────────────────────────────────────────────

def build_nav_entries(
    python_mds: list[tuple[str, Path]],
    scala_md: Path,
) -> str:
    """
    Buduje sekcję nav YAML dla diagramów.

    Args:
        python_mds: Lista (nazwa_modułu, ścieżka_md) dla Pythona.
        scala_md: Ścieżka do zbiorczego .md dla Scali.

    Returns:
        Blok YAML jako string gotowy do wklejenia w nav.
    """
    lines = ["    - Diagramy Python:"]
    for name, md_path in sorted(python_mds):
        rel = md_path.relative_to(ROOT / "docs")
        lines.append(f"          - {name}: {rel}")

    lines.append("    - Diagramy Scala:")
    rel_scala = scala_md.relative_to(ROOT / "docs")
    lines.append(f"          - Wszystkie diagramy: {rel_scala}")

    return "\n".join(lines)


def update_mkdocs_nav(python_mds: list[tuple[str, Path]], scala_md: Path) -> None:
    """
    Aktualizuje sekcję nav w mkdocs.yml — zastępuje bloki Diagramów lub dodaje nowe.

    Nie rusza żadnych innych sekcji w pliku.

    Args:
        python_mds: Lista (nazwa_modułu, ścieżka_md) dla Pythona.
        scala_md: Ścieżka do zbiorczego .md dla Scali.
    """
    content = MKDOCS_YML.read_text(encoding="utf-8")
    new_entries = build_nav_entries(python_mds, scala_md)

    # Usuń istniejące sekcje Diagramów jeśli istnieją
    content = re.sub(
        r"    - Diagramy Python:.*?(?=    - [A-ZŁŚĆĄ]|\Z)",
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"    - Diagramy Scala:.*?(?=    - [A-ZŁŚĆĄ]|\Z)",
        "",
        content,
        flags=re.DOTALL,
    )

    # Dodaj przed ostatnią pozycją nav (Moduł Scali)
    content = content.replace(
        "    - Moduł Scali (API):",
        f"{new_entries}\n    - Moduł Scali (API):",
    )

    MKDOCS_YML.write_text(content, encoding="utf-8")
    print(f"\n  [nav]    Zaktualizowano: mkdocs.yml")


# ── Główna logika ──────────────────────────────────────────────────────────────

def main() -> None:
    print("=== Generowanie diagramów ===\n")

    # Python
    print("-- Python --")
    python_mds: list[tuple[str, Path]] = []
    for py_file in get_python_modules():
        png = generate_python_diagram(py_file)
        if png:
            md = create_python_md(py_file, png)
            python_mds.append((py_file.stem, md))

    # Scala
    print("\n-- Scala --")
    scala_pngs = copy_scala_diagrams()
    scala_md = create_scala_md(scala_pngs)
    if not scala_pngs:
        print("  [Scala]  Brak PNG (sbt doc nie był uruchomiony) — utworzono placeholder")

    # mkdocs.yml
    print("\n-- mkdocs.yml --")
    if python_mds:
        update_mkdocs_nav(python_mds, scala_md)
    else:
        print("  [nav]    Brak diagramów Python — nav bez zmian")

    print("\n=== Gotowe ===")


if __name__ == "__main__":
    main()
