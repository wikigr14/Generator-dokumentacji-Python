package payment

/**
 * Strategia płatności za pośrednictwem systemu PayPal.
 *
 * Konkretna implementacja traitu [[PaymentStrategy]].
 * Odpowiada za symulację logiki transferu środków przez konto PayPal.
 *
 * ==Przykład użycia==
 * {{{
 * val strategy: PaymentStrategy = new PayPalPayment("user@example.com")
 * val result = strategy.pay(49.99)
 * // result: "Zapłacono 49.99 PLN przez PayPal (konto: user@example.com)."
 * }}}
 *
 * @param email Adres e-mail powiązany z kontem PayPal.
 * @see [[PaymentStrategy]]
 * @see [[CreditCardPayment]]
 */
class PayPalPayment(email: String) extends PaymentStrategy {

  /**
   * Realizuje płatność przy użyciu konta PayPal.
   *
   * Waliduje kwotę przed wykonaniem transferu.
   *
   * @param amount Kwota do zapłaty w PLN.
   * @return Szczegóły transferu z adresem e-mail konta PayPal.
   * @throws IllegalArgumentException jeśli `amount` jest mniejsze lub równe zero.
   */
  override def pay(amount: Double): String = {
    require(amount > 0, s"Kwota musi być większa od zera, otrzymano: $amount")
    s"Zapłacono $amount PLN przez PayPal (konto: $email)."
  }
}
