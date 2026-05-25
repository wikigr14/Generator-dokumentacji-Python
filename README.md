# Generator-dokumentacji-Python
Instrukcja uruchomienia projektu (Windows)
1. Tworzenie i aktywacja środowiska
Otwórz wiersz poleceń w głównym katalogu projektu i wpisz komendę, która utworzy środowisko:
python -m venv venv

Następnie aktywuj środowisko:
venv\Scripts\activate

2. Instalacja paczek
Gdy środowisko jest aktywne, zainstaluj wymagane biblioteki poleceniem:
pip install -r requirements.txt

3. Lokalny podgląd dokumentacji
Aby uruchomić dokumentację, wpisz:
mkdocs serve

Dokumentacja będzie dostępna w przeglądarce pod adresem [link]


#Generowanie dokumentacji dla kodu Scala (Scaladoc)
Wymagania systemowe do uruchomienia projektu w Scali:

Zainstalowane Java Development Kit (JDK) (np. wersja 11 lub 17). Zmienna środowiskowa JAVA_HOME musi być poprawnie skonfigurowana.

Zainstalowane narzędzie sbt (Scala Build Tool).

Aby wygenerować dokumentację, przejdź do folderu src/scala i wpisz komendę:
sbt doc

Gotowa dokumentacja zostanie wygenerowana w lokalizacji: src/scala/target/scala-2.13/api/index.html.
