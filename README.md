# Generator Dokumentacji Python/Scala (Projekt 18)

Automatyczny system CI/CD generujący ustandaryzowaną, wielojęzykową dokumentację z kodu źródłowego, zintegrowany z procesem release.

## Architektura Rozwiązania

Projekt wykorzystuje nowoczesny stos technologiczny do centralizacji dokumentacji:

- **Python:** Generowanie dokumentacji z docstringów za pomocą `mkdocstrings`.
- **Scala:** Generowanie natywnego API za pomocą `Scaladoc` (przez `sbt doc`).
- **Centralizacja:** Ustandaryzowany portal zbudowany w oparciu o `MkDocs` i motyw `Material for MkDocs`.
- **Wersjonowanie:** Narzędzie `mike` do utrzymywania historii wersji dokumentacji równolegle z wydaniami kodu.
- **Automatyzacja:** Przepływ pracy GitHub Actions nasłuchujący na zmiany w kodzie oraz nowe wydania (Releases).

## Jak to działa?

Z perspektywy programisty proces jest całkowicie przezroczysty. Nie wymaga ręcznego uruchamiania żadnych komend lokalnie.

1.  **Push kodu:** Programista wypycha zmiany do gałęzi `main` (lub dedykowanych gałęzi testowych).
2.  **Generowanie `latest`:** GitHub Actions automatycznie buduje kod obu języków, kompiluje zunifikowany portal i aktualizuje podgląd wersji `latest`.
3.  **Release:** Kiedy w repozytorium zostaje opublikowane nowe wydanie (GitHub Release z tagiem, np. `v1.0.0`), system tworzy trwały zrzut dokumentacji (snapshot) pod tym samym numerem wersji, widoczny z poziomu selektora na stronie.

## Rozwój lokalny

Jeśli chcesz przetestować zmiany w strukturze strony na swoim systemie (np. używając Arch Linuxa), wykonaj poniższe kroki:

```bash
# Utworzenie i aktywacja środowiska wirtualnego
python -m venv venv
source venv/bin/activate

# Instalacja zależności dla MkDocs
pip install mkdocs-material mkdocstrings[python] mike

# Uruchomienie lokalnego serwera deweloperskiego (nasłuchuje na bieżąco)
mkdocs serve
```
