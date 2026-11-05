"""
test_tsp.py

Controlli automatici di tsp.py: lo scenario 1 (un furgone grande)
risolto per enumerazione completa.
"""

import os
import sys
import unittest

# I moduli stanno in src/: aggiungo la cartella al percorso di ricerca.
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../pw23-consegne
sys.path.insert(0, os.path.join(CARTELLA_PROGETTO, "src"))                       # .../pw23-consegne/src

from istanza import carica_istanza
from tsp import risolvi_tsp


class TestTsp(unittest.TestCase):

    def setUp(self):
        # setUp viene eseguito prima di ogni test: carico i dati veri e
        # risolvo lo scenario 1 (120 giri, una frazione di secondo).
        istanza = carica_istanza(os.path.join(CARTELLA_PROGETTO, "data"))
        self.tsp = risolvi_tsp(istanza)

    def test_enumerazione_completa(self):
        self.assertEqual(self.tsp["soluzioni_generate"], 120)   # 5! = 5 x 4 x 3 x 2 x 1

    def test_giro_ottimo(self):
        # Somma -> Golasecca -> Vergiate -> Arsago -> Casorate -> Cardano -> Somma
        self.assertEqual(self.tsp["percorso"], [0, 3, 4, 1, 2, 5, 0])
        self.assertEqual(self.tsp["km"], 37.4)        # gia' arrotondato a 1 decimale da tsp.py
        self.assertEqual(self.tsp["minuti"], 116)     # 66 di guida + 5 scarichi da 10
        self.assertEqual(self.tsp["carico"], 55)      # tutte le cassette su un solo furgone

    def test_nessun_ordine_entro_60_minuti(self):
        # Tra tutti i 120 ordini, il meglio possibile per l'ultimo cliente e' 92 minuti:
        # con un solo furgone il limite di 60 minuti non si rispetta per tutti.
        self.assertEqual(self.tsp["minimo_ultimo_arrivo"], 92)


if __name__ == "__main__":
    unittest.main()
