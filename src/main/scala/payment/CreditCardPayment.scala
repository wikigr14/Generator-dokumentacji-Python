package payment

/**
 * Strategia płatności kartą kredytową.
 *
 * Konkretna implementacja traitu [[PaymentStrategy]].
 * Odpowiada za symulację logiki autoryzacji i pobierania środków z karty kredytowej.
 *
 * ==Przykład użycia==
 * {{{
 * val strategy: PaymentStrategy = new CreditCardPayment("4111111111111111")
 * val result = strategy.pay(99.99)
 * // result: "Zapłacono 99.99 PLN kartą kredytową (nr: ****1111)."
 * }}}
 *
 * @param cardNumber Numer karty kredytowej (16 cyfr). Używany wyłącznie do maskowania w potwierdzeniu.
 * @see [[PaymentStrategy]]
 * @see [[PayPalPayment]]
 */
class CreditCardPayment(cardNumber: String) extends PaymentStrategy {

  /**
   * Ostatnie 4 cyfry numeru karty, używane w potwierdzeniu transakcji.
   */
  private val maskedNumber: String = cardNumber.takeRight(4)

  /**
   * Realizuje płatność przy użyciu karty kredytowej.
   *
   * Waliduje kwotę przed wykonaniem transakcji. Maskuje numer karty
   * w zwracanym komunikacie ze względów bezpieczeństwa.
   *
   * @param amount Kwota do zapłaty w PLN.
   * @return Szczegóły transakcji z zamaskowanym numerem karty.
   * @throws IllegalArgumentException jeśli `amount` jest mniejsze lub równe zero.
   */
  override def pay(amount: Double): String = {
    require(amount > 0, s"Kwota musi być większa od zera, otrzymano: $amount")
    s"Zapłacono $amount PLN kartą kredytową (nr: ****$maskedNumber)."
  }
}
