# -*- coding: utf-8 -*-
"""
Modul do wczytywania piosenki
"""

print("Laduje modul o nazwie: "+__name__)

#import numpy as np
#import scipy.io.wavfile
#import scipy.signal

def wczytywanie_piosenki(nazwa_piosenki = "song.txt"):
    # 
    #dac asserty i doctringa ''''''
    #okreslic jakos lokalizacje skad ma brac te pliki ze z tego samego folderu gdzie jest program z katalogu 
    # odpowiedniego dla utworu - jesli w ogole, bo jedno to wczytanie pliku o takiej nazwie, a drugie skad - 
    # chyba automatycznie wczytuje z miejsca skad uruchomil sie python??
    """
    bedzie wczytywac zawartosc pliku song.txt do np.array zlozonego z macierzy n (liczba wierszy w song.txt) 
    na 1 - 1 wiersz bedzie odpowiadal jednemu trackowi - zapisane to bedzie jako string
    
    arg:
    nazwa_piosenki - nazwa pliku tekstowego wraz z rozszerzeniem, typ: str, assert - ze nie podano stringa
    reszta (ze podano zla sciezke zajmie sie genfromtxt)
    """
    
    import numpy as np

    
    song = np.genfromtxt(nazwa_piosenki,dtype='str')
    
    
    return song
    
#a = wczytywanie_piosenki()

def wczytywanie_sciezek(nazwa_piosenki):
    #dac asserty i doctringa ''''''
    #okreslic jakos lokalizacje skad ma brac te pliki ze z tego samego folderu gdzie jest program z katalogu 
    # odpowiedniego dla utworu
    
    # robimy z '01' napis 'track01.txt' by taki plik wczytac
    """
    bedziemy na podstawie pliku song.txt wczytywac tracki, typ: numpy.ndarray, i zapiszemy je jako jedna 
    macierz - zlaczymy w calosc
    
    
    
    assert, ze nie ten typ
    
    arg:
    nazwa_piosenki - np. array
    
    wyjscie:
    macierz typu np.ndarray kazdy wiersz to jedna cwiercnuta, elementy wiersza jako stringi
    """
    import numpy as np
    
    
    
    # ta funkcja zwraca np.ndarray, ktorego elementy sa juz posortowane; zakladam, ze sciezki ktore, sa podane
    # w song.txt maja numery odpowiadajace ich liczbie, tj. jak mam 3 rozne sciezki w song.txt to ich nazwy to
    # track01.txt, track02.txt, track03.txt, a nie np. track11.txt, track01.txt, track07.txt, to zalozenie
    # potrzebne dalej
    jakie_sciezki = np.unique(nazwa_piosenki)
    
    ile_sciezek = len(jakie_sciezki)
    
    #lista zwykla do trzymania sciezek, sciezka[0] - track01 (iterator trza cofnac)
    sciezki = []
    
    
    for ktora_sciezka in jakie_sciezki: # w iteratorze bierzemy napis "01" "02" itd. string!!!
        plik = ''.join(['track',ktora_sciezka,'.txt']) # tworzymy napis z nazwa pliku tracka,tj "track01.txt"
        #iterator ktora_sciezka przebiega po kolei numery (posortowane sa po unique)
        s = np.genfromtxt(plik, dtype='str')
        sciezki.append(s) # wczytujemy dane z niego
    
          
    piosenka = []
    for ktora_sciezka in nazwa_piosenki:       
        piosenka.append(sciezki[int(ktora_sciezka)-1])
    
    #zliczamy ile jest kanalow ( kolumn w trackach)
    ile_kanalow = sciezki[0].shape[1] # licze ile kolumn w plikach jest
    
    #zliczamy ile mamy cwiercnut
    n = 0
    for i in nazwa_piosenki:
        
        n += sciezki[int(i)-1].shape[0]
    
    #tworzymy z listy typ np.ndarray, ktory bedzie mial odpowiednie wymiary
    piosenka = np.array(piosenka).reshape(n, ile_kanalow)
    
    
    
    
    
    return piosenka
    
    
# machnąc w forze ze jak ktorys z trackow ma rozna liczbe kolumn to wywal blad albo
# sprawdzanie co jest w piluk to juz inna funkcja
