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
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../pw23-consegne
sys.path.insert(0, os.path.join(CARTELLA_PROGETTO, "src"))                       # .../pw23-consegne/src

from domande import calcola_domande


class TestDomande(unittest.TestCase):

    def test_resti_piu_grandi(self):
        # Abitanti ISTAT al 1/1/2025, 55 cassette in tutto.
        # Il dizionario e' scritto a mano (non letto da nodi.csv): cosi' il
        # test controlla SOLO il calcolo di domande.py, non la lettura dei file.
        # Bastano "ruolo" e "abitanti": sono le uniche chiavi che la funzione usa.
        nodi = {
            0: {"ruolo": "deposito", "abitanti": 0},   # il deposito non deve ricevere cassette
            1: {"ruolo": "cliente", "abitanti": 4735},    # Arsago Seprio
            2: {"ruolo": "cliente", "abitanti": 5596},    # Casorate Sempione
            3: {"ruolo": "cliente", "abitanti": 2635},    # Golasecca
            4: {"ruolo": "cliente", "abitanti": 8646},    # Vergiate
            5: {"ruolo": "cliente", "abitanti": 14715},   # Cardano al Campo
        }
        domande = calcola_domande(nodi, 55)
        # Parti intere 7, 8, 3, 13, 22 = 53; le 2 cassette mancanti vanno ai
        # resti piu' grandi: Golasecca (0,99) e Casorate (0,47).
        # Il confronto tra dizionari controlla anche che non ci sia la chiave 0.
        self.assertEqual(domande, {1: 7, 2: 9, 3: 4, 4: 13, 5: 22})
        self.assertEqual(sum(domande.values()), 55)   # nessuna cassetta persa o aggiunta


if __name__ == "__main__":
    unittest.main()
