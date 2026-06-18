"""
Moduł kalkulatora.

Dostarcza hierarchię klas do wykonywania operacji matematycznych.
Zbudowany zgodnie z wzorcem projektowym Template Method — klasa bazowa
definiuje szkielet algorytmu, klasy pochodne dostarczają konkretne operacje.

Hierarchia klas:
    Calculator (abstrakcyjna)
    ├── BasicCalculator       — dodawanie, odejmowanie
    ├── ScientificCalculator  — potęgowanie, pierwiastek, logarytm
    └── MemoryCalculator      — operacje z pamięcią (M+, M-, MR, MC)
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Calculator(ABC):
    """
    Abstrakcyjna klasa bazowa kalkulatora.

    Definiuje wspólny interfejs dla wszystkich typów kalkulatorów.
    Przechowuje historię wykonanych operacji.

    Attributes:
        _history (list[str]): Lista zapisanych operacji w formacie czytelnym dla człowieka.
    """

    def __init__(self) -> None:
        self._history: list[str] = []

    @abstractmethod
    def calculate(self, a: float, b: float, operation: str) -> float:
        """
        Wykonuje operację matematyczną na dwóch liczbach.

        Args:
            a (float): Pierwsza liczba (lewy operand).
            b (float): Druga liczba (prawy operand).
            operation (str): Nazwa operacji do wykonania.

        Returns:
            float: Wynik operacji.

        Raises:
            ValueError: Jeśli operacja nie jest obsługiwana przez dany kalkulator.
        """

    def get_history(self) -> list[str]:
        """
        Zwraca historię wykonanych operacji.

        Returns:
            list[str]: Kopia listy historii operacji.
        """
        return list(self._history)

    def clear_history(self) -> None:
        """Czyści historię operacji."""
        self._history.clear()

    def _record(self, entry: str) -> None:
        """Zapisuje wpis do historii operacji."""
        self._history.append(entry)


class BasicCalculator(Calculator):
    """
    Kalkulator podstawowy — cztery działania arytmetyczne.

    Dziedziczy po klasie `Calculator`. Obsługuje operacje:
    ``add``, ``subtract``, ``multiply``, ``divide``.

    Example:
        >>> calc = BasicCalculator()
        >>> calc.calculate(10, 3, "divide")
        3.3333333333333335
        >>> calc.get_history()
        ['10.0 / 3.0 = 3.3333333333333335']
    """

    SUPPORTED_OPERATIONS = ("add", "subtract", "multiply", "divide")

    def calculate(self, a: float, b: float, operation: str) -> float:
        """
        Wykonuje podstawową operację arytmetyczną.

        Args:
            a (float): Pierwsza liczba.
            b (float): Druga liczba.
            operation (str): Jedna z: ``add``, ``subtract``, ``multiply``, ``divide``.

        Returns:
            float: Wynik operacji.

        Raises:
            ValueError: Jeśli operacja nie jest obsługiwana.
            ZeroDivisionError: Jeśli ``b == 0`` przy operacji ``divide``.
        """
        if operation == "add":
            result = a + b
            self._record(f"{a} + {b} = {result}")
        elif operation == "subtract":
            result = a - b
            self._record(f"{a} - {b} = {result}")
        elif operation == "multiply":
            result = a * b
            self._record(f"{a} * {b} = {result}")
        elif operation == "divide":
            if b == 0:
                raise ZeroDivisionError("Dzielenie przez zero jest niedozwolone.")
            result = a / b
            self._record(f"{a} / {b} = {result}")
        else:
            raise ValueError(
                f"Nieobsługiwana operacja: '{operation}'. "
                f"Dostępne: {self.SUPPORTED_OPERATIONS}"
            )
        return result

    def add(self, a: float, b: float) -> float:
        """Dodaje dwie liczby. Skrót dla ``calculate(a, b, 'add')``."""
        return self.calculate(a, b, "add")

    def subtract(self, a: float, b: float) -> float:
        """Odejmuje ``b`` od ``a``. Skrót dla ``calculate(a, b, 'subtract')``."""
        return self.calculate(a, b, "subtract")

    def multiply(self, a: float, b: float) -> float:
        """Mnoży dwie liczby. Skrót dla ``calculate(a, b, 'multiply')``."""
        return self.calculate(a, b, "multiply")

    def divide(self, a: float, b: float) -> float:
        """
        Dzieli ``a`` przez ``b``. Skrót dla ``calculate(a, b, 'divide')``.

        Raises:
            ZeroDivisionError: Jeśli ``b == 0``.
        """
        return self.calculate(a, b, "divide")


class ScientificCalculator(BasicCalculator):
    """
    Kalkulator naukowy — rozszerza `BasicCalculator` o funkcje matematyczne.

    Dziedziczy wszystkie operacje podstawowe i dodaje:
    ``power``, ``sqrt``, ``log``, ``sin``, ``cos``.

    Example:
        >>> calc = ScientificCalculator()
        >>> calc.calculate(2, 10, "power")
        1024.0
        >>> calc.sqrt(144)
        12.0
    """

    def calculate(self, a: float, b: float, operation: str) -> float:
        """
        Wykonuje operację naukową lub deleguje do kalkulatora podstawowego.

        Args:
            a (float): Pierwsza liczba (lub jedyna dla operacji unarnych).
            b (float): Druga liczba (lub wykładnik/podstawa).
            operation (str): Jedna z operacji podstawowych lub ``power``, ``log``.

        Returns:
            float: Wynik operacji.

        Raises:
            ValueError: Jeśli operacja nie jest obsługiwana.
        """
        if operation == "power":
            result = math.pow(a, b)
            self._record(f"{a} ^ {b} = {result}")
            return result
        if operation == "log":
            if a <= 0:
                raise ValueError("Logarytm wymaga liczby dodatniej.")
            result = math.log(a, b) if b > 0 else math.log(a)
            self._record(f"log({a}, {b}) = {result}")
            return result
        return super().calculate(a, b, operation)

    def sqrt(self, a: float) -> float:
        """
        Oblicza pierwiastek kwadratowy z ``a``.

        Args:
            a (float): Liczba nieujemna.

        Returns:
            float: Pierwiastek kwadratowy.

        Raises:
            ValueError: Jeśli ``a < 0``.
        """
        if a < 0:
            raise ValueError("Pierwiastek z liczby ujemnej jest niezdefiniowany.")
        result = math.sqrt(a)
        self._record(f"sqrt({a}) = {result}")
        return result

    def sin(self, angle_deg: float) -> float:
        """
        Oblicza sinus kąta podanego w stopniach.

        Args:
            angle_deg (float): Kąt w stopniach.

        Returns:
            float: Sinus kąta.
        """
        result = math.sin(math.radians(angle_deg))
        self._record(f"sin({angle_deg}°) = {result}")
        return result

    def cos(self, angle_deg: float) -> float:
        """
        Oblicza cosinus kąta podanego w stopniach.

        Args:
            angle_deg (float): Kąt w stopniach.

        Returns:
            float: Cosinus kąta.
        """
        result = math.cos(math.radians(angle_deg))
        self._record(f"cos({angle_deg}°) = {result}")
        return result


class MemoryCalculator(BasicCalculator):
    """
    Kalkulator z pamięcią — rozszerza `BasicCalculator` o rejestr pamięci.

    Umożliwia zapisywanie i odczytywanie wartości z pamięci (wzorowane
    na klawiszach M+, M-, MR, MC klasycznych kalkulatorów).

    Attributes:
        _memory (float): Wartość aktualnie przechowywana w pamięci.

    Example:
        >>> calc = MemoryCalculator()
        >>> calc.memory_store(42.0)
        >>> calc.memory_recall()
        42.0
        >>> calc.memory_add(8.0)
        >>> calc.memory_recall()
        50.0
    """

    def __init__(self) -> None:
        super().__init__()
        self._memory: float = 0.0

    def memory_store(self, value: float) -> None:
        """
        Zapisuje wartość do pamięci (MS).

        Args:
            value (float): Wartość do zapisania.
        """
        self._memory = value
        self._record(f"MS: {value}")

    def memory_recall(self) -> float:
        """
        Odczytuje wartość z pamięci (MR).

        Returns:
            float: Wartość przechowywana w pamięci.
        """
        self._record(f"MR: {self._memory}")
        return self._memory

    def memory_add(self, value: float) -> None:
        """
        Dodaje wartość do pamięci (M+).

        Args:
            value (float): Wartość do dodania do pamięci.
        """
        self._memory += value
        self._record(f"M+: {value} → pamięć = {self._memory}")

    def memory_subtract(self, value: float) -> None:
        """
        Odejmuje wartość od pamięci (M−).

        Args:
            value (float): Wartość do odjęcia od pamięci.
        """
        self._memory -= value
        self._record(f"M-: {value} → pamięć = {self._memory}")

    def memory_clear(self) -> None:
        """Zeruje pamięć (MC)."""
        self._memory = 0.0
        self._record("MC: pamięć wyczyszczona")
