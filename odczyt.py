# -*- coding: utf-8 -*-
"""
Modul do wczytywania piosenki (wczytywanie song.txt i trackXY.txt oraz
tworzenie jednego obiektu na ich podstawie (numpy.ndarray (str) ) )
"""

print("Laduje modul o nazwie: "+__name__)

#import numpy as np
#import scipy.io.wavfile
#import scipy.signal

def wczytywanie_piosenki(nazwa_piosenki = "song.txt"):

    """
    wczytuje zawartosc pliku song.txt do macierzy numpy-owej
    
    arg:
        str: nazwa_piosenki - nazwa pliku tekstowego wraz z rozszerzeniem 
                              (zakladam, tak jak w opisie projektu, ze bedziemy
                              korzystac z domyslnej wartosci, tj. "song.txt", 
                              wiec nie sprawdzam poprawnosci typu tego 
                              argumentu; problemem z brakiem tego pliku etc. 
                              zajmie sie juz python, wyrzucajac komunikat, 
                              wiec tez pomijam)
    
    wyjscie:
        numpy.ndarray (str: U2): song - macierz wymiaru 1 na k (ilosc wierszy w
                                        pliku song.txt), zawierajaca kolejne
                                        wiersze z wejsciowego pliku zapisane 
                                        jako stringi
                                      
    """
    
    import numpy as np

    song = np.genfromtxt(nazwa_piosenki,dtype='str')
    
    return song
    
#a = wczytywanie_piosenki()

def wczytywanie_sciezek(lista_trackow):
    
    """
    wczytuje na podstawie pliku "song.txt" (lub innego, ktory definiował 
    liste trackow) zawartosc plikow "trackXY.txt" do jednej macierzy numpy-owej 
    
    arg:
        numpy.ndarray (str: U2): lista_trackow - macierz wymiaru 1 na k, 
                                                 zawierajaca zapisane jako 
                                                 napisy numery kolejnych 
                                                 sciezek do odtworzenia
    
    wyjscie:
        tuple: numpy.ndarray (str: U2): piosenka - macierz, zawierajaca jako
                                                   wiersze kolejne cwiercnuty 
                                                   utworu, w kazdym wierszu 
                                                   informacja czy dany sample 
                                                   ma zagrac czy nie, zapisana 
                                                   jako napis (albo numer 
                                                   sampla albo --)
        bool: dobre_trackusie - zmienna kontrolujaca poprawnosc wczytywanych 
                                trackow (metrum i ilosc sampli)
                                            
    """
    
    import numpy as np
    
    # zapisujemy unikalne numery trackow, ktore maja byc wczytane
    jakie_sciezki = np.unique(lista_trackow)

    # slownik, ktorego kolejne elementy to unikalne sciezki (key) wraz z ich 
    # zawartoscia (value)
    sciezki = {}
    
    # zmienna do sprawdzenia czy zachowane jest odpowiednie metrum (liczba 
    # wierszy podzielna przez 4) w kazdej ze sciezek, jesli nie, to zwracana 
    # macierz bedzie zerowa
    czy_4_na_4 = True
    
    # zmienna do sprawdzenia czy w kazdym tracku uzyto tyle samo sampli, jesli 
    # nie, zwracana macierz bedzie zerowa
    czy_tyle_samo_sampli = True
    
    # lista zawierajaca ilosc uzytych sampli w kolejnych trackach
    ile_sampli = []
    
    # cale to definiowanie slownika i szukanie unikalnych trackow po to by raz 
    # wczytac zawartosc uzywanych trackow a potem sie do niej odwolywac, a nie 
    # wczytywac za kazdym razem od nowa zawartosc trackow
    
    for ktora_sciezka in jakie_sciezki: # w iteratorze sa napisy "01", "02" itd
        
        # tworzymy napis z nazwa pliku tracka, np. "track01.txt"
        plik = ''.join(['track',ktora_sciezka,'.txt'])
        # wczytujemy zawartosc danego tracka do odpowiednio nazwanego elementu 
        # w slowniku sciezki
        sciezki[ktora_sciezka] = np.genfromtxt(plik, dtype='str')
        # dodajemy ilosc kanalow danego tracka do listy
        ile_sampli.append(sciezki[ktora_sciezka].shape[1])
        # sprawdzamy podzielnosc wierdzy danego tracka przez 4, jesli nie 
        # zachodzi, drukujemy odpowiedni komunikat i zmieniamy wartosc zmiennej 
        # logicznej czy_4_na_4 na False
        if(sciezki[ktora_sciezka].shape[0] % 4 != 0):
            print("Plik: ", plik, " nie ma podzielnej przez 4 liczby wierszy")
            czy_4_na_4 = False

    
    # sprawdzamy czy ilosc uzytych sampli jest taka sama w kazdym tracku
    # set-em wyciagamy unikalne wartosci i sprawdzamy czy jest tylko jedna taka
    if(len(set(ile_sampli))!=1): 
        print("Rozna liczba uzytych sampli w trackach")
        czy_tyle_samo_sampli = False
    
    # jedna zmienna odpowiadajaca za poprawnosc trackow
    dobre_trackusie = czy_4_na_4 and czy_tyle_samo_sampli
    
    # jesli metrum i ilosc sampli sie zgadza zapisujemy zawartosc sciezek w 
    # piosence do numpy.ndarraya
    if(dobre_trackusie):
 
            # do zapisu poslugujemy sie lista i funkcja append na liscie, gdyz 
            # jest to bardziej efektywne niz append dla numpy.ndarraya, gdy nie
            # znamy jego ostatecznych rozmiarow
            piosenka = []
            
            # np.genfromtxt inaczej zapisuje plik gdy jest 1 linijka, wiec
            # inaczej dostajemy sie do jego zawartosci
            if(lista_trackow.size ==1):
                #dodajemy odpowiednia wartosc ze slownika sciezki
                piosenka.append(sciezki[str(lista_trackow)]) 

                #tworzymy z listy obiekt typu numpy.ndarray
                piosenka = np.array(piosenka)
                # obiekt ten zawiera kilka podmacierzy, wiec tworzymy z niego 
                # 1 macierz
                piosenka = np.vstack(piosenka)
            else:
                # tym razem iterujemy po kolejnych trackach z lista_trackow, 
                # nie po unikalnych nazwach trackow
                for ktora_sciezka in lista_trackow:
                    #dodajemy odpowiednia wartosc ze slownika sciezki
                    piosenka.append(sciezki[ktora_sciezka])

                #tworzymy z listy obiekt typu numpy.ndarray
                piosenka = np.array(piosenka)
                # obiekt ten zawiera kilka podmacierzy, wiec tworzymy z niego 
                # 1 macierz
                piosenka = np.vstack(piosenka)
    # gdy nie ma odpowiedniego metrum lub ilosci sampli zwracamy zerowa macierz      
    else: 
        piosenka = np.array([0])

    return piosenka, dobre_trackusie 

# pios, k = wczytywanie_sciezek(a)
