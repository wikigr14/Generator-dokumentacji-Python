package example

/**
 * Główny obiekt aplikacji.
 * * Służy do testowania lokalnego generowania dokumentacji za pomocą Scaladoc.
 */
object Hello {

  /**
   * Metoda witająca użytkownika.
   *
   * @param name Imię użytkownika.
   * @return Powitanie w formie tekstowej.
   */
  def greeting(name: String): String = {
    s"Witaj, $name!"
  }
}