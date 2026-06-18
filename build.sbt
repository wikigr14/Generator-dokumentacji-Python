name := "Projekt18-Scala"
version := "0.1"
scalaVersion := "2.13.12"

// Włącza generowanie grafów dziedziczenia w Scaladoc.
// Wymaga zainstalowanego Graphviz (apt-get install graphviz) na maszynie budującej.
Compile / doc / scalacOptions ++= Seq(
  "-diagrams",
  "-diagrams-dot-path", "/usr/bin/dot"
)
