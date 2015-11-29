Popraw!

dodatkowe informacje o programie (m.in. opis plików, rozszerzeń itp.)

Ogolnie zakladam, ze pliki tekstowe song.txt, trackXY.txt i defs.txt sa
poprawnie sformatowane (1 wiersz - 1 sciezka, etc.) i niepuste - sprawdzam 
tylko pojedyncze zalozenia (np. czy ilosc wierszy jest podzielna przez 4,
czy tyle samo kolumn w kazdym z trackow), ktore moga wyniknac z mojej nieuwagi

Plik utwor1.wav itd. zapisuje sie w /tmp/


Uzywam funkcji numpy.genfromtxt, ktora ma bugga (chyba) gdy wczytywany plik
tekstowy ma tylko jedna linijke - trzeba wtedy inaczej dostawac sie do 
zawartosci wczytanego pliku (nie for-em po wierszach, jak w przypadku wielu 
linii)
