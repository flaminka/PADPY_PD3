#!/usr/bin/env python
"""
Program glowny - OPIS UZUPELNIC
#!/opt/anaconda34/bin/python3 - zmienic interpreter
#!/home/rexamine/anaconda/bin/python
"""

#1 tak by uruchamiało się jako ./beatbox utwor1
#2 wczytac podany przez uzytkownika katalog

import odczyt
import zapis

#import importlib
#importlib.reload(modul1)



#zakladam, ze lokalizacja z ktorej bedzie brac pliki to ta w ktorej jest
# beatbox.py

#jako argument przekazujemy utwor1/ 

if __name__=='__main__':
    import sys
    # zapisuje nazwe folderu z trackami
    utwor = sys.argv[1] 
    
    # zmieniam sciezke workspace'a
    import os
    folder = ''.join([os.getcwd(),'/',utwor])
    os.chdir(folder)
    
    #wczytujemy tracki w jedna dluga macierz
    macierz_song = odczyt.wczytywanie_sciezek(odczyt.wczytywanie_piosenki())
    
    #wczytujemy ustawienia
    parametry = zapis.wczytywanie_ustawien()
    
    #zapisujemy utwor w numpy array
    pioseneczka = zapis.tworzenie_piosenki(macierz_song, parametry['bpm'])
    
    #import numpy as np
    import scipy.io.wavfile
    #import scipy.signal
    
    # ustawiamy sciezke dostepu do tmp 
    folder_tmp = '/tmp/'
    import re

    nazwa_pliku = ''.join([folder_tmp,re.sub('/','',utwor),'.wav'])  
    
    scipy.io.wavfile.write(nazwa_pliku, 
                           44100,
                           pioseneczka
                           )