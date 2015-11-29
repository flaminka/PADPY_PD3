# -*- coding: utf-8 -*-
"""
Modul do zapisu piosenki (wczytywanie ustawien (defs.txt), tworzenie .wav,
                          "zglasnianie utworu")
"""


print("Laduje modul o nazwie: "+__name__)

import numpy as np

def wczytywanie_ustawien(plik_konfiguracyjny = "defs.txt"):
    """ 
    wczytywanie pliku z ustawieniami (pliku defs.txt) do slownika
    
    arg:
        str: plik_konfiguracyjny - nazwa pliku konfiguracyjnego z podanymi 
                                   wartosciami parametrow (tempo itd.)
        
    wyjscie:
        dict: parametry - zapisane nazwy i wartosci uzywanych parametrow
    
    """
    import re
    import numpy as np
    
    # wczytuje zawartosc pliku (bez pierwszej i ostatniej linijki, jeden wiersz 
    # wyjsciowej macierzy, zawiera nazwe parametru i jego wartosc, jako 
    # oddzielne elementy, zapisane jako stringi)
    ustawienia = np.genfromtxt(plik_konfiguracyjny, dtype = str, \
                               skip_header=1, skip_footer=1, delimiter=":")
    
    # tworze slownik, ktory bedzie przechowywal wartosci
    parametry = {}
    
    # pozbywam się "" z key
    
    # jesli mamy 1 parametr (1 linijka w pliku, to ustawienia to zmienna o 
    # shape = (2,), wiec odwoluje sie bezposrednio do zmiennej ustawienia
    if ustawienia.shape == (2,): 
        parametry[re.sub('"','',ustawienia[0])] = ustawienia[1]
    # jak mamy wiecej parametrow odwoluje sie do kolejnych linijek macierzy 
    # ustawienia
    else:
        for l in ustawienia:  
            parametry[re.sub('"','',l[0])] = l[1]
    
    # zamieniamy napisy na odpowiednie wartosci - kontroluje te parametry, wiec
    # robie to recznie
    try:
        parametry['bpm'] = int(parametry['bpm']) # tempo
        parametry['freq'] = int(parametry['freq']) # frekwencja wyjsciowego wav
        parametry['loud'] = float(parametry['loud'] ) # glosnosc
        # lista wag dla sampli
        parametry['wages'] = [float(s) for s in parametry['wages'].split(",")] 
    
    # jak nie podano danego parametru to idz dalej, nie wyrzucaj bledu
    except KeyError:
        pass
    
    return parametry
    
#b = wczytywanie_ustawien("defs.txt")
    
    
#zglasnianie utworu

def zmiana_glosnosci(utwor, procent = 0):
    """
    zmienia glosnosc utworu (jego amplitudy)
    
    arg:
        numpy.ndarray (numpy.int16): utwor - dzwiek, ktory ma byc zglosniony 
                                             lub zciszony
        
        float: procent - liczba obrazujaca zmiane glosnosci utworu, osiaga 
                         wartosci od -1 do 1, dla 0 brak zmian, dla 1 - "100% 
                         glosniej", dla -1 "100% ciszej"
    
    wyjscie:
        numpy.ndarray (numpy.int16): glosniejszy -sciszony lub zglosniony utwor
    """
    if(-1 <= procent <= 1):
        #ile razy mamy pomnozyc amplitude naszego dzwieku
        mnoznik = 0
        if( procent < 0 ):
            mnoznik = 1 + procent
        else:
            # obliczamy najwyzsza amplitude w danym utworze i ona bedzie 
            # wyznaczac jak bardzo mozemy podglosnic
            maks_ampli = 0
            maks_ampli = max(abs(utwor))
            mnoznik = 32767/maks_ampli # maksymalny mnoznik
            # mnoznik minimalnie moze osiagnac wartosc 1, to co powyzej 
            # (mnoznik-1) mnozymy o procent zglosnienia
            # i dodajemy do podstawy (czyli 1)
            mnoznik = 1 + (mnoznik - 1)*procent
        glosniej = mnoznik * utwor
        #glosniej = np.array(glosniej, dtype=np.int16)
        glosniej = glosniej.astype(np.int16) 
        return glosniej
    else:
        print("Podaj procent z zakresu -1 do 1")
                               

#wierszyk1 = zmiana_glosnosci(wierszyk, b['loud'])
#wierszyk1
    
    
    

def tworzenie_piosenki(macierz_piosenki, czy_pelna = True, bpm = 120, \
                       freq = 44100, wages = None, loud = 0):
    """
    glowna funkcja generujaca cala piosenke
    
    arg:
        numpy.ndarray (str: U2): macierz_piosenki - macierz zawierajaca 
                                 definicje kolejnych cwiercnut (co ma byc grane 
                                 w danej cwiercnucie)
                                 
        bool: czy_pelna - zmienna sprawdzajaca czy macierz_piosenki jest 
                          zapisana (nie jest, gdy tracki mialy nieodpowiednia 
                          liczbe wierszy lub kolumn)
                          
        int: bpm - tempo piosenki w jednostce bpm
        
        int: freq - ilosc probek w jednej sekundzie
        
        list (float): wages - wagi kolejnych sampli (jakie znaczenie ma miec 1 
                              probka, 2 etc.)
                              
        float: loud - procent glosnosci, 0 - tak jak oryginalne probki, 1 - na 
                      maxa, -1 - sciszamy na maxa
    
    wyjscie:
        numpy.ndarray (numpy.int16): gotowy utwór
        
    """
    
    
    # macierz piosenki byla pusta, piosenka nie zostala utworzona
    if(czy_pelna == False):
        print("Nie utworzono piosenki")
        return None 
    
    else:
    
        import numpy as np
        import scipy.io.wavfile
        
        t_cwiercnuty = 60 / bpm # czas trwania jednej cwiercnuty (zalezy od 
                                                                  #tempa)
        ile_cwiercnut = macierz_piosenki.shape[0] # ilosc cwiercnut
        kanaly = macierz_piosenki.shape[1] # ilosc uzywanych sampli
        frekw = freq
        czas_utworu = ile_cwiercnut*t_cwiercnuty
        # ile elementow bedzie w nowym utworze
        ilosc_probek = int(frekw*czas_utworu) 
        
        # bedziemy tylko raz wczytywac zawartosc sampleXY.wav, wiec potrzebuje 
        # unikalne numery sampli
        rozne_sample = np.unique(macierz_piosenki) # bierze lacznie z "--"
        
        # w slownikach zapiszemy parametry tych sampli
        # slownik z wartosciami danego sampla (tj. macierze numpy-owe z 
        # amplitudami)
        sample_co = {} 
        sample_frekw = {} # slownik z ich frekwencjami
        sample_dl = {} # slownik z ich dlugosciami
        
        #wczytujemy te sample
        # w iteratorze bierzemy napisy "01" "02"  "--" itd. stringi!!!
        for ktory_sampel in rozne_sample: 
        
            if(ktory_sampel != '--'):
                # tworzymy napis z nazwa pliku sampla, np. "sample01.wav"
                plik = ''.join(['sample',ktory_sampel,'.wav'])
                # wczytujemy zawartosc i frekwencje danego sampla do 
                # odpowiednio nazwanego elementu w slowniku sample_co i 
                # sample_frekw
                sample_frekw[ktory_sampel], sample_co[ktory_sampel] = \
                                                    scipy.io.wavfile.read(plik)
                # tworzymy mono z naszego sampla
                sample_co[ktory_sampel] = np.mean(sample_co[ktory_sampel],\
                                                                axis=1)/32767
                # normalizujemy te wartosci
                sample_co[ktory_sampel] = np.int16(sample_co[ktory_sampel]/ \
                                  max(np.abs(sample_co[ktory_sampel])) * 32767)
                # zapisujemy dlugosc sampli, czyli ilosc probek 
                # ( = czas_trwania*frekwencja)
                sample_dl[ktory_sampel] = sample_co[ktory_sampel].shape[0]
                
            else: # to samo robimy dla "--" recznie ustawiamy
                # robimy cisze, gdy --
                sample_co[ktory_sampel] = np.zeros((1,), dtype=np.int16) 
                sample_frekw[ktory_sampel] = frekw # taka sama jak domyslna
                sample_dl[ktory_sampel] = 0 # zakladamy czas 0 sekund
         

        
        
 
        if wages is None:
            wages = np.ones((1,kanaly))  
        else:
            # zeby mialo wymiar (1,kanaly), a nie (kanaly,)
            wages = np.array(wages).reshape(1,kanaly)       
        
        # definicja nowego utworu
        T = np.linspace(0, czas_utworu, ilosc_probek)
        
        for wiersz in range(0, ile_cwiercnut):

            sample = [] # wczytamy sample z danej cwiecnuty
            dlugosci = [] # tu zapiszemy ich dlugosci w tej cwiercnucie

            for i in range(0, kanaly):
                
                sampus = macierz_piosenki[wiersz,i]
                sample.append(sample_co[sampus])   
                dlugosci.append(sample_dl[sampus])

                    
            # bierzemy najdluzszy sample i w calosci bedziemy go odtwarzac; 
            # reszte zatem tez w calosci odtworzymy, a gdy sie skoncza damy 
            # cisze (zera)
            maksik = max(dlugosci)
            # mamy tutaj macierz 4 na max dlugosc, przygotowana do zlaczenia 
            # potem tych dzwiekow w jeden 
            pusty = np.int16(np.zeros((len(sample), maksik)))

            # dodajemy nasze dzwieki do tej pustej
            for k in range(0, kanaly):
                pusty[k][0:dlugosci[k]] = sample[k]

           
            # mnozymy kolejne elementy wektora pusty (czyli sample) przez 
            # wagi i sumujemy
            cwiercnuta = np.dot(wages, pusty) 
            #otrzymamy wymiar (1, x), a chcemy (x,), wiec bierzemy pierwszy 
            # element
            cwiercnuta = cwiercnuta[0]
                        
            # jesli dodanie ostatnich cwiercnut bedzie wiazalo sie z 
            # przekroczeniem dlugosci tworzonego utworu, obcinamy ostatnie 
            # dzwieki, tak by zmiescic sie w tej dlugosci
            
            # poczatek biezacej cwiercnuty 
            poczatek_cwiercnuty = int(wiersz*t_cwiercnuty*frekw)
            
            # jesli dodanie ostatnich cwiercnut bedzie wiazalo sie z 
            # przekroczeniem dlugosci tworzonego utworu, obcinamy ostatnie 
            # dzwieki, tak by zmiescic sie w tej dlugosci
            if (poczatek_cwiercnuty + maksik) > ilosc_probek:
                
                T[poczatek_cwiercnuty:(poczatek_cwiercnuty + maksik)]=\
                cwiercnuta[0:len(T[poczatek_cwiercnuty:(poczatek_cwiercnuty +\
                                                                    maksik)])]
                
            else:
                T[poczatek_cwiercnuty:(poczatek_cwiercnuty + maksik)] += \
                                                                     cwiercnuta
        
        T= np.array(T, dtype=np.int16)
        
        #ustalamy glosnosc utworu
        T = zmiana_glosnosci(T, loud)

        return T

#pios, k = wczytywanie_sciezek(a)
#wierszyk = tworzenie_piosenki(pios, k, bpm = b['bpm'], freq = b['freq'], \
#wages = b['wages'])
#wierszyk = tworzenie_piosenki(pios, k, **b)
#wierszyk 