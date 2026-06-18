# Architektura systemu

Diagramy klas generowane automatycznie z kodu źródłowego w ramach potoku CI/CD.

## Wzorzec Strategii — moduł płatności

Struktura wzorca Strategy zaimplementowanego w `src/python/pattern.py`:

- `PaymentStrategy` — abstrakcyjna klasa bazowa definiująca kontrakt
- `CreditCardPayment` — implementacja płatności kartą kredytową
- `PayPalPayment` — implementacja płatności przez PayPal
