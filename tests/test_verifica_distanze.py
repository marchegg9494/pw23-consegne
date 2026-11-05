"""
test_verifica_distanze.py

Controlli automatici di verifica_distanze.py: il confronto tra le
distanze rilevate su Google Maps e la matrice ISTAT.
"""

import os
import sys
import unittest

# I moduli stanno in src/: aggiungo la cartella al percorso di ricerca.
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../pw23-consegne
sys.path.insert(0, os.path.join(CARTELLA_PROGETTO, "src"))                       # .../pw23-consegne/src

from verifica_distanze import verifica_distanze


class TestVerificaDistanze(unittest.TestCase):

    def setUp(self):
        # setUp viene eseguito prima di ogni test: leggo il file di confronto vero.
        # os.path.join con piu' pezzi costruisce
        # .../pw23-consegne/data/rilevazione/verifica_istat_distanze.csv
        file_verifica = os.path.join(CARTELLA_PROGETTO, "data", "rilevazione",
                                     "verifica_istat_distanze.csv")
        self.verifica = verifica_distanze(file_verifica)   # dizionario con 6 numeri, letto dai due test

    def test_tratte_tra_clienti(self):
        # Stessi punti (municipio -> municipio): scarto piccolo.
        self.assertEqual(self.verifica["tratte_clienti"], 20)              # 30 tratte - 10 col deposito
        self.assertEqual(self.verifica["scarto_medio_clienti_km"], 0.365)  # 7,3 km di scarti / 20 tratte
        self.assertEqual(self.verifica["entro_soglia"], 16)                # 16 tratte su 20 entro 0,5 km

    def test_tratte_con_deposito(self):
        # Google parte dall'azienda, ISTAT dal municipio: Google da' piu' km.
        self.assertEqual(self.verifica["tratte_deposito"], 10)             # 5 in andata + 5 al ritorno
        self.assertEqual(self.verifica["scarto_medio_deposito_km"], 1.43)  # +14,3 km / 10 tratte, con il segno


if __name__ == "__main__":
    unittest.main()
