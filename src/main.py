"""
main.py

Punto di avvio del programma. Da eseguire dalla cartella principale
del progetto con:

    python src/main.py

Passaggi:
  1. legge i dati, calcola le domande dei clienti (domande.py)
     e controlla che tutto sia coerente (istanza.py);
  2. confronta le distanze rilevate con la matrice ISTAT (verifica_distanze.py);
  3. risolve lo scenario 1 con un veicolo (tsp.py);
  4. stampa i risultati a schermo.
"""

import os

from istanza import carica_istanza
from verifica_distanze import verifica_distanze
from tsp import risolvi_tsp
from percorsi import descrivi_percorso   # trasforma [0, 3, ...] in "Somma Lombardo -> Golasecca -> ..."


# Calcolo le cartelle partendo dalla posizione di questo file, cosi' il
# programma funziona da qualunque cartella venga lanciato.
CARTELLA_SRC = os.path.dirname(os.path.abspath(__file__))     # .../pw23-consegne/src
CARTELLA_PROGETTO = os.path.dirname(CARTELLA_SRC)               # .../pw23-consegne
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "data")         # .../pw23-consegne/data


def stampa_risultati(istanza, tsp):
    """Stampa a schermo un riepilogo leggibile delle domande e dello scenario 1."""
    nodi = istanza["nodi"]

    print("=" * 60)                                    # una riga di 60 "="
    print("DOMANDE CALCOLATE (proporzionali agli abitanti)")
    print("=" * 60)
    for id_cliente in istanza["clienti"]:
        # :<20 allinea a sinistra su 20 caratteri, :>7 a destra su 7: escono colonne ordinate
        print(f"{nodi[id_cliente]['comune']:<20} {nodi[id_cliente]['abitanti']:>7} abitanti -> {istanza['domande'][id_cliente]:>3} cassette")
    print("Totale:", sum(istanza["domande"].values()), "cassette")   # 55
    print()
    print("Criterio da minimizzare:", istanza["criterio"])          # minuti
    print()

    print("=" * 60)
    print("SCENARIO 1 - un veicolo grande (capacita'", istanza["capacita_grande"], "cassette)")
    print("=" * 60)
    print("Percorsi provati:", tsp["soluzioni_generate"])            # 120
    print("Giro ottimo:     ", descrivi_percorso(tsp["percorso"], nodi))
    print("Chilometri:      ", tsp["km"])                            # 37.4
    print("Durata (minuti): ", tsp["minuti"])                        # 116
    print("Carico:          ", tsp["carico"], "cassette")            # 55
    print()


def stampa_verifica(verifica):
    """Stampa il confronto tra le distanze di Google Maps e la matrice ISTAT."""
    print("=" * 60)
    print("CONTROLLO DELLE DISTANZE CON LA MATRICE ISTAT")
    print("=" * 60)
    print(f"Tratte tra clienti: {verifica['tratte_clienti']}, "
          f"scarto medio {verifica['scarto_medio_clienti_km']} km, "
          f"massimo {verifica['scarto_massimo_clienti_km']} km, "
          f"{verifica['entro_soglia']} entro 0,5 km")
    print(f"Tratte con il deposito: {verifica['tratte_deposito']}, "
          f"Google Maps in media {verifica['scarto_medio_deposito_km']:+} km "    # :+ mostra sempre il segno: +1.43
          f"(parte dall'azienda, ISTAT dal municipio)")
    print()


def main():
    istanza = carica_istanza(CARTELLA_DATI)            # legge e controlla i dati: se sono sbagliati si ferma qui
    verifica = verifica_distanze(
        os.path.join(CARTELLA_DATI, "rilevazione", "verifica_istat_distanze.csv"))
    tsp = risolvi_tsp(istanza)                         # prova i 120 ordini di visita
    stampa_risultati(istanza, tsp)
    stampa_verifica(verifica)


# Questo blocco fa partire main() solo quando il file viene eseguito
# direttamente (python src/main.py), e non quando viene importato.
if __name__ == "__main__":
    main()
