# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:33:59 2015

Modul do zapisu piosenki (tworzeni .wav)
"""

import numpy as np
def wczytywanie_ustawien(plik_konfiguracyjny = "defs.txt"):
    """
    asserty 
    na razie zakladam, ze wszystkie parametry beda liczbami
    
    wczytywanie pliku z ustawieniami (pliku defs.txt)
    
    arg:
        nazwa pliku konfiguracyjnego, typ: string
        
    wyjscie:
        wartosci parametrow zapisane w slowniku, typ: dict
    
    """
    import re
    # wczytuje zawartowsc pliku (bez pierwszej i ostatniej linijki, jeden wiersz wyjsciowej macierzy, zawiera
    # nazwe parametru i jego wartosc, jako oddzielne elementy, zapisane jako stringi)
    ustawienia = np.genfromtxt(plik_konfiguracyjny, dtype = str,skip_header=1,skip_footer=1, delimiter=":")
    # tworze slownik, ktory bedzie przechowywal wartosci
    parametry = {}
    # tworze slownik
    # pozbywam się "" z key i przerabiam value na inty
    if len(ustawienia) == 2:
        parametry[re.sub('"','',ustawienia[0])] = int(ustawienia[1])
    else:
        for l in ustawienia:
        
            parametry[re.sub('"','',l[0])] = int(l[1])
    
    # zwracam gotowy slownik
    return parametry
#b = wczytywanie_ustawien()

# NOWE PRZERÓBKA
def tworzenie_piosenki(macierz_piosenki, bpmy = 120):
    """
    asserty 
    glowna funkcja
    """
    
    t_cwiercnuty = 60 / bpmy
    n = macierz_piosenki.shape[0]
    kanaly = macierz_piosenki.shape[1]
    
    import numpy as np
    import scipy.io.wavfile
    import scipy.signal
    
    # utwor
    T = np.linspace(0, n*t_cwiercnuty, 44100*n*t_cwiercnuty)
        
    
    for wiersz in range(0, 10): # ZMIEN TU NA N ZAMIAST 10
        
        sample = []
        dlugosci = []
        
        for i in range(0, kanaly):
            
            if macierz_piosenki[wiersz,i] == '--':
                sample.append(np.zeros((1,1)))    
            else:
                plik = ''.join(['sample', macierz_piosenki[wiersz,i],'.wav']) 
                frekw, t = scipy.io.wavfile.read(plik)
                sample.append(t)
                sample[i] = np.mean(sample[i], axis=1)/32767 # robi mono
                sample[i] = np.int16(sample[i]/max(np.abs(sample[i]))*32767)
                dlugosci.append(sample[i].shape[0])
        
        maksik = max(dlugosci)
        pusty = np.int16(np.zeros((len(sample), maksik)))
        for k in range(0, len(sample)):
            pusty[k][0:sample[k].shape[0]] = sample[k]
                
        cwiercnuta = sum(pusty)
        if (wiersz*t_cwiercnuty*44100 + maksik) > len(T):
            T[wiersz*t_cwiercnuty*44100:(wiersz*t_cwiercnuty*44100 + maksik)]= cwiercnuta[0:len(T[wiersz*t_cwiercnuty*44100:(wiersz*t_cwiercnuty*44100 + maksik)])]
        else:
            T[wiersz*t_cwiercnuty*44100:(wiersz*t_cwiercnuty*44100 + maksik)]= cwiercnuta
        
    T= np.array(T, dtype=np.int16)
    return T


#wierszyk = tworzenie_piosenki(wczytywanie_sciezek(a), b['bpm'])
#wierszyk
