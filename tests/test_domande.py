"""
test_domande.py

Controlli automatici di domande.py: la ripartizione delle 55 cassette
tra i cinque clienti con il metodo dei resti piu' grandi.

Si lancia dalla cartella principale con:
    python3 -m unittest discover tests

Il test confronta il risultato di calcola_domande con i valori riportati
nel rapporto: se fallisce, qualcosa nei dati o nel codice e' cambiato e
il rapporto non e' piu' coerente.
"""

import os
import sys
import unittest

# I moduli stanno in src/: aggiungo la cartella al percorso di ricerca.
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CARTELLA_PROGETTO, "src"))

from domande import calcola_domande


class TestDomande(unittest.TestCase):

    def test_resti_piu_grandi(self):
        # Abitanti ISTAT al 1/1/2025, 55 cassette in tutto.
        nodi = {
            0: {"ruolo": "deposito", "abitanti": 0},
            1: {"ruolo": "cliente", "abitanti": 4735},
            2: {"ruolo": "cliente", "abitanti": 5596},
            3: {"ruolo": "cliente", "abitanti": 2635},
            4: {"ruolo": "cliente", "abitanti": 8646},
            5: {"ruolo": "cliente", "abitanti": 14715},
        }
        domande = calcola_domande(nodi, 55)
        self.assertEqual(domande, {1: 7, 2: 9, 3: 4, 4: 13, 5: 22})
        self.assertEqual(sum(domande.values()), 55)


if __name__ == "__main__":
    unittest.main()
