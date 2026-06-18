# Dokumentacja API — Wzorzec Strategii

Automatycznie wygenerowana dokumentacja modułu `pattern.py`, implementującego
wzorzec projektowy **Strategia** (Strategy Pattern).

---

## Przykład użycia

Poniżej przykład zastosowania wzorca w obu językach — logika jest identyczna,
różni się tylko składnia:

=== "Python"

    ```python
    from pattern import CreditCardPayment, PayPalPayment

    # Wybór strategii w zależności od preferencji użytkownika
    strategy = CreditCardPayment()
    print(strategy.pay(99.99))
    # Zapłacono 99.99 PLN przy użyciu karty kredytowej.

    strategy = PayPalPayment()
    print(strategy.pay(49.99))
    # Zapłacono 49.99 PLN przy użyciu systemu PayPal.
    ```

=== "Scala"

    ```scala
    import payment._

    // Wybór strategii w zależności od preferencji użytkownika
    val strategy: PaymentStrategy = new CreditCardPayment("4111111111111111")
    println(strategy.pay(99.99))
    // Zapłacono 99.99 PLN kartą kredytową (nr: ****1111).

    val strategy2: PaymentStrategy = new PayPalPayment("user@example.com")
    println(strategy2.pay(49.99))
    // Zapłacono 49.99 PLN przez PayPal (konto: user@example.com).
    ```

---

## Dokumentacja klas

::: pattern.PaymentStrategy
    options:
      show_root_heading: true
      show_source: true

??? warning "Klasa abstrakcyjna — nie można instancjonować bezpośrednio"
    `PaymentStrategy` jest klasą bazową definiującą kontrakt. Zawsze używaj
    jednej z klas pochodnych: `CreditCardPayment` lub `PayPalPayment`.

---

::: pattern.CreditCardPayment
    options:
      show_root_heading: true
      show_source: true

??? info "Szczegóły implementacyjne — CreditCardPayment"
    Metoda `pay()` nie wykonuje rzeczywistej transakcji — symuluje logikę
    autoryzacji kartowej. W środowisku produkcyjnym należy zastąpić ją
    integracją z bramką płatniczą (np. Stripe, Adyen).

---

::: pattern.PayPalPayment
    options:
      show_root_heading: true
      show_source: true

??? info "Szczegóły implementacyjne — PayPalPayment"
    Metoda `pay()` symuluje transfer PayPal. W środowisku produkcyjnym
    wymaga integracji z PayPal REST API i obsługi tokenów OAuth 2.0.
