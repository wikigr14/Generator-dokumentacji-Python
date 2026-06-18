# Dokumentacja API — Wzorzec Strategii

Automatycznie wygenerowana dokumentacja modułu `pattern.py`, implementującego
wzorzec projektowy **Strategia** (Strategy Pattern).

---

## Przykład użycia

=== "Python"

    ```python
    from pattern import CreditCardPayment, PayPalPayment

    strategy = CreditCardPayment()       # (1)
    print(strategy.pay(99.99))           # (2)

    strategy = PayPalPayment()           # (3)
    print(strategy.pay(49.99))
    ```

    1. Tworzymy konkretną strategię — możemy ją podmienić w dowolnym momencie
    2. Wypisuje: `Zapłacono 99.99 PLN przy użyciu karty kredytowej.`
    3. Podmiana strategii — kod klienta się nie zmienia, zmienia się tylko obiekt

=== "Scala"

    ```scala
    import payment._

    val strategy: PaymentStrategy =      // (1)
      new CreditCardPayment("4111111111111111")
    println(strategy.pay(99.99))         // (2)

    val strategy2: PaymentStrategy =
      new PayPalPayment("user@example.com")
    println(strategy2.pay(49.99))
    ```

    1. Typ zmiennej to `PaymentStrategy` (trait), nie konkretna klasa — to sedno wzorca
    2. Wypisuje: `Zapłacono 99.99 PLN kartą kredytową (nr: ****1111).`

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
