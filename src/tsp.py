"""
tsp.py

SCENARIO 1: un solo veicolo grande, con capacita' sufficiente per tutti
i clienti.

Il problema e' un Traveling Salesman Problem (TSP, "problema del
commesso viaggiatore"): il veicolo parte dal deposito, visita tutti i
clienti una sola volta e torna al deposito. Si cerca l'ordine di visita
che rende minimo il criterio scelto (minuti o chilometri totali,
vedi "criterio_ottimizzazione" in parametri.json).

Metodo: ENUMERAZIONE COMPLETA, come richiesto dalla traccia.
Si generano TUTTI i possibili ordini di visita dei clienti, si calcolano
il valore di ognuno e si tiene il migliore.

Con n clienti gli ordini possibili sono n! (n fattoriale).
Con 5 clienti: 5! = 5 x 4 x 3 x 2 x 1 = 120 percorsi.
Il numero cresce molto in fretta (con 10 clienti sono 3.628.800),
quindi questo metodo va bene solo per istanze piccole come la nostra.
"""

from itertools import permutations   # genera tutti gli ordinamenti possibili di una lista

from percorsi import crea_percorso, km_percorso, minuti_percorso, carico_percorso, valore_percorso, orari_arrivo


def risolvi_tsp(istanza):
    """
    Prova tutti gli ordini di visita e restituisce il migliore.

    Restituisce un dizionario con:
      - percorso:  la lista dei nodi del giro ottimo
      - km:        i chilometri del giro ottimo
      - minuti:    la durata del giro (guida + scarichi)
      - carico:    cassette caricate sul veicolo
      - arrivi:    dopo quanti minuti arriva da ogni cliente
      - soluzioni_generate: quanti percorsi sono stati provati
      - minimo_ultimo_arrivo: il miglior tempo possibile di arrivo
        all'ultimo cliente, tra tutti gli ordini di visita
    """
    clienti = istanza["clienti"]                       # [1, 2, 3, 4, 5]
    km = istanza["km"]

    migliore_percorso = None                           # None = "non ho ancora trovato niente"
    miglior_valore = None
    soluzioni_generate = 0                             # contatore: alla fine 120
    # Il minimo, tra tutti gli ordini di visita, del tempo di arrivo
    # all'ULTIMO cliente: dice se con un solo furgone e' possibile
    # consegnare tutto entro il tempo massimo, qualunque ordine si scelga.
    minimo_ultimo_arrivo = None

    # permutations(clienti) genera tutte le sequenze possibili dei clienti,
    # per esempio (1, 2, 3, 4, 5), (1, 2, 3, 5, 4), ... fino a (5, 4, 3, 2, 1).
    for sequenza in permutations(clienti):             # 120 giri del ciclo
        percorso = crea_percorso(sequenza)             # (3, 4, 1, 2, 5) -> [0, 3, 4, 1, 2, 5, 0]
        valore = valore_percorso(percorso, istanza)    # con criterio "minuti": la durata del giro
        soluzioni_generate = soluzioni_generate + 1

        arrivi = orari_arrivo(percorso, istanza["minuti"], istanza["tempo_scarico"])
        ultimo_arrivo = max(arrivi.values())           # l'arrivo piu' tardi di questo giro
        if minimo_ultimo_arrivo is None or ultimo_arrivo < minimo_ultimo_arrivo:
            minimo_ultimo_arrivo = ultimo_arrivo       # alla fine: 92 minuti

        # Se e' il primo percorso che provo, o se e' migliore (valore piu'
        # basso) del migliore trovato finora, diventa il nuovo migliore.
        if miglior_valore is None or valore < miglior_valore:
            miglior_valore = valore                    # alla fine: 116 minuti
            migliore_percorso = percorso               # alla fine: [0, 3, 4, 1, 2, 5, 0]

    # Nello scenario 1 non serve controllare la capacita' percorso per
    # percorso: il carico e' sempre la domanda totale, e istanza.py ha
    # gia' verificato che entra nel veicolo grande.
    risultato = {
        "percorso": migliore_percorso,
        "km": round(km_percorso(migliore_percorso, km), 1),                       # 37.4
        "minuti": round(minuti_percorso(migliore_percorso, istanza["minuti"], istanza["tempo_scarico"])),   # 116
        "carico": carico_percorso(migliore_percorso, istanza["domande"]),        # 55
        "arrivi": orari_arrivo(migliore_percorso, istanza["minuti"], istanza["tempo_scarico"]),   # {3: 13, 4: 33, 1: 56, 2: 73, 5: 92}
        "soluzioni_generate": soluzioni_generate,                                # 120
        "minimo_ultimo_arrivo": minimo_ultimo_arrivo,                            # 92
    }
    return risultato

