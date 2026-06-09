from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    """
    Klasa abstrakcyjna (interfejs) dla strategii płatności.

    Definiuje wspólny kontrakt dla wszystkich metod płatności obsługiwanych 
    w systemie. Implementuje wzorzec projektowy Strategy.
    """

    @abstractmethod
    def pay(self, amount: float) -> str:
        """
        Przetwarza płatność na podaną kwotę.

        Args:
            amount (float): Kwota do zapłaty.

        Returns:
            str: Komunikat potwierdzający status płatności.
        """
        pass

class CreditCardPayment(PaymentStrategy):
    """
    Strategia płatności kartą kredytową.

    Dziedziczy po klasie `PaymentStrategy`. Odpowiada za symulację logiki 
    autoryzacji i pobierania środków z karty kredytowej.
    """

    def pay(self, amount: float) -> str:
        """
        Realizuje płatność przy użyciu karty kredytowej.

        Args:
            amount (float): Kwota do zapłaty.

        Returns:
            str: Szczegóły transakcji kartą kredytową.
        """
        return f"Zapłacono {amount} PLN przy użyciu karty kredytowej."

class PayPalPayment(PaymentStrategy):
    """
    Strategia płatności za pośrednictwem systemu PayPal.

    Dziedziczy po klasie `PaymentStrategy`. Odpowiada za symulację logiki 
    logowania do konta PayPal i transferu środków.
    """

    def pay(self, amount: float) -> str:
        """
        Realizuje płatność przy użyciu konta PayPal.

        Args:
            amount (float): Kwota do zapłaty.

        Returns:
            str: Szczegóły transakcji w systemie PayPal.
        """
        return f"Zapłacono {amount} PLN przy użyciu systemu PayPal."