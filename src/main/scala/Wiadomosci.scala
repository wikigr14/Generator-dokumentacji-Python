package wiadomosci

/**
 * Główny obiekt do obsługi wiadomości w systemie.
 * Zapewnia metody do formatowania i wyświetlania powitań.
 */
object GeneratorWiadomosci {

  /**
   * Generuje spersonalizowane powitanie.
   *
   * @param imie Imię użytkownika do przywitania.
   * @return Sformatowany ciąg znaków z powitaniem.
   */
  def powitaj(imie: String): String = {
    s"Witaj, $imie! Dokumentacja Scali działa poprawnie."
  }
}
