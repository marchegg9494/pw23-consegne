"""
verifica_distanze.py

Confronta le distanze rilevate a mano su Google Maps con la matrice
ufficiale ISTAT delle distanze tra comuni, per controllare che i dati
usati dal programma siano attendibili.

Il file letto e' data/rilevazione/verifica_istat_distanze.csv, che per
ogni tratta riporta affiancati i km di Google Maps e i km ISTAT
(campo KM_TOT della matrice ISTAT, grafo stradale 2020).

Punti di riferimento usati nella rilevazione su Google Maps:
  - deposito (nodo 0): l'azienda agricola, Via Eugenio Villoresi 140;
  - clienti (nodi 1-5): il municipio di ciascun comune.
ISTAT invece usa sempre il municipio, anche per Somma Lombardo.

Per questo le tratte sono divise in due gruppi:
  - tratte tra clienti (es. Golasecca -> Vergiate): Google Maps e ISTAT
    vanno entrambi da municipio a municipio, quindi i km devono essere
    quasi uguali. Si misura lo scarto medio IN VALORE ASSOLUTO (conta
    quanto sono lontani, non in che direzione) e quante tratte
    differiscono al massimo di 0,5 km;
  - tratte con il deposito (es. deposito -> Golasecca): Google Maps parte
    dall'azienda, ISTAT dal municipio di Somma Lombardo. Qui lo scarto e'
    atteso e si misura CON IL SEGNO: un valore positivo vuol dire che
    Google Maps da' piu' km di ISTAT.

Esempio di scarto per tre tratte:
    da 3 a 4 (Golasecca -> Vergiate):  Google 4,8 km, ISTAT 4,9 km -> scarto -0,1 (assoluto 0,1)
    da 4 a 3 (Vergiate -> Golasecca):  Google 6,9 km, ISTAT 5,6 km -> scarto  1,3 (senso unico)
    da 0 a 1 (deposito -> Arsago):     Google 4,8 km, ISTAT 2,9 km -> scarto +1,9
"""

import csv   # legge il file CSV riga per riga

from istanza import ID_DEPOSITO   # 0: serve per riconoscere le tratte con il deposito


# Soglia per dire che una tratta "coincide" con ISTAT: 0,5 km.
SOGLIA_KM = 0.5


def verifica_distanze(percorso_file):
    """
    Legge il file di confronto e restituisce un dizionario con:
      - tratte_clienti:           numero di tratte tra due clienti (20)
      - scarto_medio_clienti_km:  media dello scarto in valore assoluto
      - scarto_massimo_clienti_km: scarto piu' grande tra clienti
      - entro_soglia:             tratte tra clienti con scarto <= 0,5 km
      - tratte_deposito:          tratte da o verso il deposito (10)
      - scarto_medio_deposito_km: media dello scarto con il segno
    """
    tratte_clienti = 0
    somma_scarti_clienti = 0                           # somma dei valori assoluti
    scarto_massimo_clienti = 0
    entro_soglia = 0
    tratte_deposito = 0
    somma_scarti_deposito = 0                          # somma con il segno

    with open(percorso_file, encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        for riga in lettore:                           # riga = {"da": "3", "a": "4", "km_google_maps": "4.8", "km_istat": "4.9", ...}
            da = int(riga["da"])
            a = int(riga["a"])
            scarto = float(riga["km_google_maps"]) - float(riga["km_istat"])   # 4,8 - 4,9 = -0,1

            if da == ID_DEPOSITO or a == ID_DEPOSITO:  # tratta che parte o arriva al deposito
                tratte_deposito = tratte_deposito + 1
                somma_scarti_deposito = somma_scarti_deposito + scarto   # con il segno
            else:                                      # tratta tra due clienti
                tratte_clienti = tratte_clienti + 1
                scarto_assoluto = abs(scarto)          # abs(-0,1) = 0,1
                somma_scarti_clienti = somma_scarti_clienti + scarto_assoluto
                if scarto_assoluto > scarto_massimo_clienti:
                    scarto_massimo_clienti = scarto_assoluto
                # Arrotondo a 1 decimale (come i dati) prima del confronto:
                # 2,2 - 1,7 in Python da' 0,5000000000000002, non 0,5.
                if round(scarto_assoluto, 1) <= SOGLIA_KM:
                    entro_soglia = entro_soglia + 1

    return {
        "tratte_clienti": tratte_clienti,                                          
        "scarto_medio_clienti_km": round(somma_scarti_clienti / tratte_clienti, 3),   
        "scarto_massimo_clienti_km": round(scarto_massimo_clienti, 1),             
        "entro_soglia": entro_soglia,                                              
        "tratte_deposito": tratte_deposito,                                        
        "scarto_medio_deposito_km": round(somma_scarti_deposito / tratte_deposito, 2), 
    }

