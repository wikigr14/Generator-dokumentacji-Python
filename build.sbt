name := "Projekt18-Scala"
version := "0.1"
scalaVersion := "2.13.12"

enablePlugins(ClassDiagramPlugin)

// Flaga -diagrams generuje interaktywne grafy dziedziczenia w Scaladoc HTML
Compile / doc / scalacOptions ++= Seq(
  "-diagrams",
  "-diagrams-dot-path", "/usr/bin/dot"
)
