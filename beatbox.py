"""
Program glowny - OPIS UZUPELNIC
"""
#najpierw zrobie wszystko w jednym pliku a potem bede myslec


#### PLAN:
#1 tak by uruchamiało się jako ./beatbox utwor1
#2 wczytac podany przez uzytkownika katalog
#if __name__=='__main__':
#    import sys
#    print(sys.argv)
#3 w tym katalogu wyszukac plik song i go wczytac linijka po linijce (for)
#4 kazdda linijka powinna nas zmusic do wywolania pliku track0X (wczytanie pliku
# ktorego nazwa to track+01), potem kolejna petla
# i teraz w tej petli wczytywac 4 sample (wg nazwy tez) i laczyc je w jedna sek???
# nowego utworu, wg tempa jakiegos jeszcze zrobic to plusami y =  +  +  +
# potem wychpdznimy z drugiej petli i dodajemy te y do juz istnialego itd.
# w koncu mamy ostateczne y i to y zapisujemy do pliku












#if __name__=='__main__':
#    import sys
#    print(sys.argv)

#   WCZYTYWANIE PLIKOW
#with open(...) as f:
#    for line in f:
# ALBO     content = f.readlines()













#### ZAPIS DO .WAV  - do zapisu utworzonego utworu jako .wav


# Wynikiem działania programu jest plik utworX.wav (nazwa taka jak katalogu 
# wejściowego.
#import scipy.io.wavfile
#y = np.r_[dzwiek(440*S**(-2), 0.5, 0.2,0.2),
#          dzwiek(440*S**(-5), 0.5, 0.2,0.2),
#          dzwiek(440*S**(-5), 0.5, 0.2,0.2)]
#scipy.io.wavfile.write('/home/samba/baranowskae/Desktop/test.wav', 
#                           fs,
#                           np.int16(y/max(np.abs(y))*32767)
#                          )     