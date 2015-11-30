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
import nuty

#import importlib
#importlib.reload(modul1)



#zakladam, ze lokalizacja z ktorej bedzie brac pliki to ta w ktorej jest
# beatbox.py

#jako argument przekazujemy utwor1/ 

if __name__=='__main__':
    import sys
    # zapisuje nazwe folderu z trackami
    argument = sys.argv[1] 
    
    import os    
    import re
    import zipfile
   # ustawiamy sciezke dostepu do tmp 
    folder_tmp = '/tmp/'    
    
    try: # gdy mamy utwor1.zip
    #zakladam kodowanie 'latin-1' bo wtedy nie wywalalo mi bledu
    #jesli chcialabym poszukac kodowania, to musialabym wziac liste wszystkich
    #mozliwosci
    #from encodings.aliases import aliases
    # aliases.items()       
    #i iterowac po nich forem z try-em, ale na razie naiwnie zakladam, ze to 
    #co u mnie dziala, bedzie dzialac gdzie indziej
        f = open(argument, 'r', encoding='latin-1') 
        poczatek = f.read(10)
        #sprawdzam czy zip poprzez magic number dla niego
        if poczatek.startswith("\x50\x4b\x03\x04"):
            zipek = zipfile.ZipFile(argument)
            zipek.extractall(folder_tmp)
            zipek.close()
            # wyciagam nazwe utworu
            nazwa_utworu = re.sub('.zip','',argument)
            folder = ''.join([folder_tmp, nazwa_utworu, '/'])
            # zmieniam sciezke workspace'a
            os.chdir(folder)  
            # zapisuje nazwe utworu jako wav
            nazwa_pliku = ''.join([folder_tmp, nazwa_utworu, '.wav'])
        f.close()
    except UnicodeDecodeError:
        print("Nie to kodowanie :/")
    except IsADirectoryError: # gdy mamy utwor1/
        folder = ''.join([os.getcwd(),'/',argument])
        # zmieniam sciezke workspace'a
        os.chdir(folder)
        nazwa_pliku = ''.join([folder_tmp, re.sub('/','',argument), '.wav'])
        
        
    
    #wczytujemy ustawienia
    parametry = zapis.wczytywanie_ustawien()    
    
    if parametry['tryb'] == 'nutki':
        
        ustawienia = { 'bpm' : parametry['bpm'],\
                       'freq' : parametry['freq'], \
                       'loud' : parametry['loud'], \
                       'slownik_nut' : nuty.tworzenie_nutek()}
        
        #wczytujemy tracki w jedna dluga macierz i zapisuje czy tracki byly ok
        macierz_song = nuty.wczytywanie_sciezek_nuty(\
                                                odczyt.wczytywanie_piosenki())
    
        #zapisujemy utwor w numpy array
        pioseneczka = nuty.tworzenie_piosenki_nuty(macierz_song, **ustawienia)
        
        
        
    if parametry['tryb'] == 'sample':
        
        ustawienia = { 'bpm' : parametry['bpm'],\
                       'freq' : parametry['freq'], \
                       'wages': parametry['wages'],\
                       'loud' : parametry['loud']}
        
        #wczytujemy tracki w jedna dluga macierz i zapisuje czy tracki byly ok
        macierz_song, ok = odczyt.wczytywanie_sciezek(\
                                                odczyt.wczytywanie_piosenki())
    
        #zapisujemy utwor w numpy array
        pioseneczka = zapis.tworzenie_piosenki(macierz_song, ok, **ustawienia)
       
    
    
    
    #import numpy as np
    import scipy.io.wavfile
    #import scipy.signal
    

    # zapisujemy plik w folderze tmp pod odpowiednia nazwa
    scipy.io.wavfile.write(nazwa_pliku, 
                           parametry['freq'],
                           pioseneczka
                           )