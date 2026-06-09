"""
Moduł kalkulatora.

Ten moduł dostarcza podstawowe operacje matematyczne.
Stanowi przykład do automatycznego generowania dokumentacji.
"""

def add(a: float, b: float) -> float:
    """
    Dodaje dwie liczby do siebie

    Args:
        a (float): Pierwsza liczba.
        b (float): Druga liczba.

    Returns:
        float: Suma liczb `a` i `b`.
    """
    return a + b

def subtract(a: float, b: float) -> float:
    """
    Odejmuje drugą liczbę od pierwszej.

    Args:
        a (float): Odjemna.
        b (float): Odjemnik.

    Returns:
        float: Różnica liczb `a` i `b`.
    """
    return a - b