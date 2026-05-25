@echo off
echo Budowanie dokumentacji Scala...
cd src\scala
call sbt doc
cd ..\..

echo Kopiowanie plikow Scaladoc do folderu docs...
xcopy src\scala\target\scala-2.13\api\* docs\scaladoc\ /E /I /Y

echo Gotowe! Mozesz teraz uruchomic: mkdocs serve