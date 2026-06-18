# Dokumentacja API — Kalkulator

Automatycznie wygenerowana dokumentacja modułu `calculator.py`.

---

## Przykład użycia

=== "BasicCalculator"

    ```python
    from calculator import BasicCalculator

    calc = BasicCalculator()
    print(calc.add(10, 5))       # (1)
    print(calc.divide(10, 3))    # (2)
    print(calc.get_history())    # (3)
    ```

    1. Zwraca `15.0`
    2. Zwraca `3.3333...` — wynik jest typu `float`
    3. Zwraca listę wszystkich operacji: `['10 + 5 = 15.0', '10.0 / 3.0 = 3.333...']`

=== "ScientificCalculator"

    ```python
    from calculator import ScientificCalculator

    calc = ScientificCalculator()
    print(calc.calculate(2, 10, "power"))  # (1)
    print(calc.sqrt(144))                  # (2)
    print(calc.sin(90))                    # (3)
    ```

    1. Zwraca `1024.0` — potęgowanie: 2^10
    2. Zwraca `12.0`
    3. Zwraca `1.0` — kąt podany w **stopniach**, nie radianach

=== "MemoryCalculator"

    ```python
    from calculator import MemoryCalculator

    calc = MemoryCalculator()
    calc.memory_store(100.0)              # (1)
    calc.memory_add(calc.add(20, 5))      # (2)
    print(calc.memory_recall())           # (3)
    ```

    1. Zapisuje `100.0` do pamięci (odpowiednik klawisza **MS**)
    2. Dodaje wynik `20 + 5 = 25` do pamięci — pamięć wynosi teraz `125.0`
    3. Zwraca `125.0` — odpowiednik klawisza **MR**

---

## Dokumentacja klas

::: calculator.Calculator

---

::: calculator.BasicCalculator

??? warning "Dzielenie przez zero"
    Metoda `divide()` rzuca `ZeroDivisionError` gdy drugi argument wynosi `0`.
    Zawsze waliduj dane wejściowe przed wywołaniem.

---

::: calculator.ScientificCalculator

??? info "Kąty w stopniach"
    Metody `sin()` i `cos()` przyjmują kąt w **stopniach**, nie radianach.
    Konwersja do radianów odbywa się wewnętrznie.

---

::: calculator.MemoryCalculator
