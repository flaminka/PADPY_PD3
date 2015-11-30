# -*- coding: utf-8 -*-
"""
Modul analogiczny do odczytu i zapisu razem wzietych, ale do generowania
dzwieku z podanych nut; funkcje, ktorych nie musialam zmieniac z odczyt.py lub
zapis.py by generowac taki dzwiek, zostaly tu pominiete - beda wyciagniete 
po prostu z tamtych modulow
"""
print("Laduje modul o nazwie: "+__name__)

import zapis

def tworzenie_nutek(dla_A4 = 440):
    """
    funkcja tworzaca slownik definiujacy wartosc kazdej nuty
    (zgodnie z http://www.phy.mtu.edu/~suits/notefreqs.html)
    arg:
        float: dla_A4 - jaka wartosc przypisujemy nucie A4
    
    wyjscie:
        dict: slownik_nut - gotowy slownik
    """
    wszystkie_nutki = []
    podstawa = ["C-", "C#", "D-","D#", "E-", "F-", "F#", "G-", "G#", "A-", \
                "A#", "B-"]
    
    #dodajemy numerki z tylu 
    for i in range(0,9):
        wszystkie_nutki += [''.join([x, str(i)]) for x in podstawa]
    
    S = pow(2, 1/12) #stala
    
    #wartosci kolejnych nut
    wartosci = [ dla_A4*S**(n) for n in range(-57, 50)]
    
    #krotki
    prawie_slownik = zip(wszystkie_nutki,wartosci)
    
    slownik_nut = {}
    
    #tworzymy slownik
    for nuta, amplituda in prawie_slownik:
        slownik_nut[nuta] = amplituda
        
    #cisza
    slownik_nut['---'] = 0

    return slownik_nut
    
#nutki = tworzenie_nutek()  
    
def wczytywanie_sciezek_nuty(lista_trackow):
    """
    
    wczytuje na podstawie pliku "song.txt" (lub innego, ktory definiował liste 
    trackow) zawartosc plikow "trackXY.txt" do jednej macierzy numpy-owej 
    
    arg:
        numpy.ndarray (str: U2): lista_trackow - macierz wymiaru 1 na k, 
                                                 zawierajaca zapisane jako 
                                                 napisy numery kolejnych 
                                                 sciezek do odtworzenia
    
    wyjscie:
        numpy.ndarray (str: U2): piosenka - macierz, zawierajaca jeden wiersz z
                                            kolejnymi nutami
                                  
    """
    
    import numpy as np
    
    # zapisujemy unikalne numery trackow, ktore maja byc wczytane
    jakie_sciezki = np.unique(lista_trackow)

    # slownik, ktorego kolejne elementy to unikalne sciezki (key) wraz z ich 
    # zawartoscia (value)
    sciezki = {}
    
    # cale to definiowanie slownika i szukanie unikalnych trackow po to by raz
    # wczytac zawartosc uzywanych trackow a potem sie do niej odwolywac, a nie
    # wczytywac za kazdym razem od nowa zawartosc trackow
    
    for ktora_sciezka in jakie_sciezki: # w iteratorze mamy napisy "01" "02" 
        
        # tworzymy napis z nazwa pliku tracka, np. "track01.txt"
        plik = ''.join(['track',ktora_sciezka,'.txt'])
        # wczytujemy zawartosc danego tracka do odpowiednio nazwanego elementu 
        # w slowniku sciezki
        
        # dodalam comments='&' bo traktowal # jako poczatek komentarza
        sciezki[ktora_sciezka] = np.genfromtxt(plik, dtype='str', comments="&")

 
    # do zapisu poslugujemy sie lista i funkcja append na liscie, gdyz jest to 
    # bardziej efektywne niz append dla numpy.ndarraya, gdy nie znamy jego 
    # ostatecznych rozmiarow
    piosenka = []
            
    
    if(lista_trackow.size ==1):
        #dodajemy odpowiednia wartosc ze slownika sciezki
        piosenka.append(sciezki[str(lista_trackow)]) 

        #tworzymy z listy obiekt typu numpy.ndarray
        piosenka = np.array(piosenka)
        # obiekt ten zawiera kilka podmacierzy, wiec tworzymy z niego 1 macierz
        piosenka = np.vstack(piosenka)
    else:
        # tym razem iterujemy po kolejnych trackach z lista_trackow, nie po unikalnnych 
        # nazwach trackow
        for ktora_sciezka in lista_trackow:
            #dodajemy odpowiednia wartosc ze slownika sciezki
            piosenka.append(sciezki[ktora_sciezka]) 

        #tworzymy z listy obiekt typu numpy.ndarray
        piosenka = np.array(piosenka)
        # obiekt ten zawiera kilka podmacierzy, wiec tworzymy z niego 1 macierz
        piosenka = np.hstack(piosenka)     

    return piosenka

#pios =  wczytywanie_sciezek_nuty(a)


def tworzenie_piosenki_nuty(macierz_piosenki, slownik_nut, bpm = 120, \
                            freq = 44100, loud = 0):
    """
    glowna funkcja generujaca cala piosenke z nutek
    
    arg:
        numpy.ndarray (str: U2): macierz_piosenki - macierz zawierajaca     
                                                    definicje kolejnych 
                                                    dzwiekow
        int: bpm - tempo piosenki w jednostce bpm
        int: freq - ilosc probek w jednej sekundzie
        float: loud - procent glosnosci, 0 - tak jak oryginalne probki, 1 - 
                      na maxa, -1 - sciszamy na maxa
    
    wyjscie:
        numpy.ndarray (numpy.int16): gotowy utwór
    """
    
    import numpy as np
    
    # czas trwania jednej nutki (czas trwania cwiercnuty (zalezy od tempa))
    t_cwiercnuty = 60 / bpm 
    ile_cwiercnut = macierz_piosenki.shape[0] # ilosc nutek
    frekw = freq # frekwencja
    ile_nutka = t_cwiercnuty*frekw # ile elementow w jednym dzwieku
    czas_utworu = ile_cwiercnut*t_cwiercnuty #czas trwania utworu
    ilosc_probek = int(frekw*czas_utworu) # ile elementow bedzie w utworze
    
    

    # definicja nowego utworu
    T = np.linspace(0, czas_utworu, ilosc_probek)
    
    # ktory dzwiek zapisujemy
    nr_dzwieku = 0
    # iterujemy po kolejnych nutach 'F#4' 'D-4' itd
    for dzwiek in macierz_piosenki:

        # macierz dla danej nutki okreslajaca jej czas
        t = np.linspace(0, t_cwiercnuty, ile_nutka)
        # macierz danej nutki okreslajaca jej wysokosc
        y = np.sin(2*np.pi*slownik_nut[dzwiek]*t + 0.1)
        # wstawiamy ja w odpowiednie miejsce
        T[nr_dzwieku*ile_nutka : nr_dzwieku*ile_nutka + ile_nutka] = y
        nr_dzwieku +=1
      
    # zamieniamy na odpowiednie wartosci
    T = np.int16(T/max(np.abs(T))*32767)
    
    #ustalamy glosnosc utworu
    T = zapis.zmiana_glosnosci(T, loud)

    
    return T

#pios = wczytywanie_sciezek_nuty(a)
#wierszyk = tworzenie_piosenki_nuty(pios, bpm = b['bpm'], freq = b['freq'], 
#loud = b['loud'], slownik_nut = nutki)
#wierszyk 









