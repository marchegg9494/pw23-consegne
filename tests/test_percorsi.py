"""
test_percorsi.py

Controlli automatici di percorsi.py sul giro [0, 3, 4, 0]
(Somma Lombardo -> Golasecca -> Vergiate -> Somma Lombardo),
il giro del furgone B nello scenario 2.
"""

import os
import sys
import unittest

# I moduli stanno in src/: aggiungo la cartella al percorso di ricerca.
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../pw23-consegne
sys.path.insert(0, os.path.join(CARTELLA_PROGETTO, "src"))                       # .../pw23-consegne/src

from istanza import carica_istanza   # serve per avere km, minuti e domande veri
from percorsi import crea_percorso, km_percorso, minuti_percorso, carico_percorso, orari_arrivo


class TestPercorsi(unittest.TestCase):

    def setUp(self):
        # setUp viene eseguito prima di ogni test: carico i dati veri e
        # preparo il giro su cui provare tutte le funzioni.
        self.istanza = carica_istanza(os.path.join(CARTELLA_PROGETTO, "data"))   
        self.giro = crea_percorso((3, 4))   # come in tsp.py e vrp.py: si parte da una tupla di clienti

    def test_crea_percorso(self):
        self.assertEqual(self.giro, [0, 3, 4, 0])   # deposito aggiunto all'inizio e alla fine

    def test_km_minuti_carico(self):
        # 6,4 + 4,8 + 6,8 km; 13 + 10 + 13 minuti di guida + 2 scarichi da 10.
        self.assertAlmostEqual(km_percorso(self.giro, self.istanza["km"]), 18.0)
        self.assertEqual(minuti_percorso(self.giro, self.istanza["minuti"], 10), 56)   # 36 di guida + 20 di scarico
        self.assertEqual(carico_percorso(self.giro, self.istanza["domande"]), 17)      # Golasecca 4 + Vergiate 13

    def test_orari_arrivo(self):
        # Golasecca dopo 13 minuti; Vergiate dopo 13 + 10 (scarico) + 10 = 33.
        # Il ritorno al deposito non compare: non e' una consegna.
        self.assertEqual(orari_arrivo(self.giro, self.istanza["minuti"], 10), {3: 13, 4: 33})


if __name__ == "__main__":
    unittest.main()
