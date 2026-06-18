package payment

/**
 * Trait definiujący kontrakt dla wszystkich strategii płatności.
 *
 * Implementuje wzorzec projektowy [[https://en.wikipedia.org/wiki/Strategy_pattern Strategy]].
 * Każda klasa dziedzicząca musi dostarczyć konkretną implementację metody [[pay]].
 *
 * ==Hierarchia klas==
 * {{{
 *   PaymentStrategy (trait)
 *   ├── CreditCardPayment
 *   └── PayPalPayment
 * }}}
 *
 * @see [[CreditCardPayment]]
 * @see [[PayPalPayment]]
 */
trait PaymentStrategy {

  /**
   * Przetwarza płatność na podaną kwotę.
   *
   * @param amount Kwota do zapłaty w PLN. Musi być większa od zera.
   * @return Komunikat potwierdzający status transakcji.
   * @throws IllegalArgumentException jeśli `amount` jest ujemne lub równe zero.
   */
  def pay(amount: Double): String
}
