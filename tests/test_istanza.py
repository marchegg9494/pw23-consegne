"""
test_istanza.py

Controlli automatici di istanza.py: lettura dei file in data/ e
condizioni della traccia sulle quantita'.
"""

import os
import sys
import unittest

# I moduli stanno in src/: aggiungo la cartella al percorso di ricerca.
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../pw23-consegne
sys.path.insert(0, os.path.join(CARTELLA_PROGETTO, "src"))                       # .../pw23-consegne/src

from istanza import carica_istanza


class TestIstanza(unittest.TestCase):

    def setUp(self):
        # setUp viene eseguito prima di ogni test: carico i dati veri.
        # Uso il percorso completo della cartella data/ (e non solo "data")
        # cosi' il test funziona da qualunque cartella venga lanciato.
        # self.istanza e' un attributo: lo leggono tutti i metodi test_ qui sotto.
        self.istanza = carica_istanza(os.path.join(CARTELLA_PROGETTO, "data"))   # .../pw23-consegne/data

    def test_nodi_e_tratte(self):
        self.assertEqual(len(self.istanza["nodi"]), 6)                     # deposito + 5 clienti
        tratte = sum(len(arrivi) for arrivi in self.istanza["km"].values())   # 5 tratte per ognuno dei 6 nodi
        self.assertEqual(tratte, 30)                                       # 6 x 5 = 30, le righe di distanze.csv

    def test_servono_due_veicoli(self):
        # Vincolo della traccia: un veicolo grande basta, uno piccolo no.
        totale = sum(self.istanza["domande"].values())                     # 55 cassette
        self.assertLessEqual(totale, self.istanza["capacita_grande"])      # 55 <= 60
        self.assertGreater(totale, self.istanza["capacita_piccolo"])       # 55 > 50


if __name__ == "__main__":
    unittest.main()
