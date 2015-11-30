W katalogu programu znajduja sie: 

skrypty:
beatbox.py - skrypt z glowym programem
odczyt.py - modul z funkcjami do odczytu kolejnosci sampli (z pliku song.txt,
potem z trackXY.txt)
zapis.py - modul do zapisu dzwiekow w postaci utworu (macierz numpy-owa)
nuty.py - modul do zapisu utworu na podstawie nut (korzysta z fali sinusoidalnej

foldery:
utwor1 - z definicjami odpowiednich plikow do generowania dzwieku z sampli
utwor2 - z definicjami odpowiednich plikow do generowania dzwieku z nut
utwor3 - z definicjami odpowiednich plikow do generowania dzwieku z nut

archiwum:
utwor1.zip - ze spakowanym katalogem utwor1, do sprawdzenia czy dziala odzipowanie

Ogolnie zakladam, ze pliki tekstowe song.txt, trackXY.txt i defs.txt sa
poprawnie sformatowane (1 wiersz - 1 sciezka, etc.) i niepuste - sprawdzam 
tylko pojedyncze zalozenia (np. czy ilosc wierszy jest podzielna przez 4,
czy tyle samo kolumn w kazdym z trackow), ktore moga wyniknac z mojej nieuwagi

Pliki utwor1.wav itd. zapisywane sa w /tmp/

Uzywam funkcji numpy.genfromtxt, ktora gdy wczytywany plik tekstowy ma tylko 
jedna linijke wymaga innego potraktowania jej wyniku - trzeba wtedy inaczej 
dostawac sie do zawartosci wczytanego pliku (nie for-em po wierszach, jak w 
przypadku wielu linii)

Warto by pokusic sie kiedys o wyeliminowanie tzw. efektu dread audio cliff of noise
czyli tego klikania przy dzwiekach generowanych z nut.
