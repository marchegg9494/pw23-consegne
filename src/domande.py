"""
domande.py

Calcola quante cassette consegnare a ogni cliente.

Perche' "domande": nel Vehicle Routing Problem la quantita' che un cliente
deve ricevere si chiama DOMANDA (in inglese "demand") e si indica con q_i.
Il vincolo di capacita' dice che la somma delle domande dei clienti di un
giro non puo' superare la capacita' Q del veicolo. Nello scenario di questo
progetto la domanda corrisponde all'ordine del cliente (cassette per
consegna), ma non e' un ordine reale: e' una stima, spiegata qui sotto.

L'azienda oggi non effettua consegne, quindi non esistono ordini reali.
Le quantita' sono un'IPOTESI del progetto, costruita cosi':

  1) si fissa il totale di cassette di un giro di consegna
     (parametro "cassette_totali_giro" in parametri.json);
  2) il totale viene diviso tra i clienti in proporzione agli abitanti
     del loro comune (dati ISTAT nel file nodi.csv):

         quota_i = totale x abitanti_i / somma_abitanti

  3) le quote non sono numeri interi (non si consegna mezza cassetta),
     quindi vanno arrotondate. Per far si' che la somma resti esattamente
     uguale al totale si usa il METODO DEI RESTI PIU' GRANDI:
       - a ogni cliente si assegna la parte intera della sua quota;
       - le cassette che mancano per arrivare al totale vanno, una per
         uno, ai clienti con la parte decimale (il "resto") piu' grande.

Esempio con totale 55 (abitanti dei 5 comuni: 36.327 in tutto):
    Cardano:   quota 22,28 -> parte intera 22, resto 0,28
    Vergiate:  quota 13,09 -> parte intera 13, resto 0,09
    Golasecca: quota  3,99 -> parte intera  3, resto 0,99
    ...
    Somma delle parti intere = 53, mancano 2 cassette:
    vanno ai 2 resti piu' grandi (Golasecca 0,99, Casorate 0,47).
"""

import math

def calcola_domande(nodi, totale_cassette): # riceve i nodi (con numero abitanti) & totale cassette

    # Considero solo i clienti (il deposito non riceve merce).
    clienti = [id_nodo for id_nodo in nodi if nodi[id_nodo]["ruolo"] == "cliente"]   # -> [1, 2, 3, 4, 5]
    clienti.sort()                                     # ordine fisso: risultato sempre uguale

    somma_abitanti = 0                                 # contatore che parte da zero
    for id_cliente in clienti:
        somma_abitanti = somma_abitanti + nodi[id_cliente]["abitanti"]   # alla fine: 36.327

    # 1) Quota esatta di ogni cliente e sua parte intera.
    domande = {}                                       # cassette (intere)
    resti = {}                                         # parte decimale delle cassette persa
    for id_cliente in clienti:
        quota = totale_cassette * nodi[id_cliente]["abitanti"] / somma_abitanti   # Golasecca: 55 x 2635 / 36327 = 3,99
        domande[id_cliente] = math.floor(quota)        # Golasecca: 3
        resti[id_cliente] = quota - math.floor(quota)  # Golasecca: 3,99 - 3 = 0,99

    # 2) Quante cassette mancano per arrivare al totale.
    mancanti = totale_cassette - sum(domande.values()) # 55 - 53 = 2

    # 3) Ordino i clienti dal resto piu' grande al piu' piccolo e do
    #    una cassetta in piu' ai primi "mancanti" della lista.
    clienti_per_resto = sorted(clienti, key=lambda id_cliente: resti[id_cliente], reverse=True)   # -> [3, 2, 5, 1, 4]
    for i in range(mancanti):
        domande[clienti_per_resto[i]] = domande[clienti_per_resto[i]] + 1   # Golasecca 3 -> 4, Casorate 8 -> 9

    return domande
