"""
percorsi.py

Piccole funzioni di supporto usate sia dallo scenario 1 (Traveling Salesman Problem) sia dallo
scenario 2 (Vehicle Routing Problem). 

In tutto il programma, un "percorso" (o "giro") e' una lista di id di nodi
che parte dal deposito e torna al deposito, per esempio:
    [0, 3, 4, 1, 0]
significa: Somma Lombardo -> Golasecca -> Vergiate -> Arsago Seprio -> Somma Lombardo
"""

from istanza import ID_DEPOSITO   # 0


def crea_percorso(sequenza_clienti):
    """
    Data una sequenza di clienti, per esempio (3, 4, 1), restituisce il
    percorso completo con il deposito all'inizio e alla fine:
    [0, 3, 4, 1, 0].
    """
    return [ID_DEPOSITO] + list(sequenza_clienti) + [ID_DEPOSITO]   # [0] + [3, 4] + [0] = [0, 3, 4, 0]


def km_percorso(percorso, km):
    """
    Somma i chilometri di tutte le tratte del percorso.

    Esempio con percorso [0, 3, 4, 0]:
        km[0][3] + km[3][4] + km[4][0]
    Ogni tratta va dal nodo in posizione i al nodo in posizione i+1.
    """
    totale = 0
    for i in range(len(percorso) - 1):                 # 4 nodi -> 3 tratte: i = 0, 1, 2
        da = percorso[i]                               # i = 0: da = 0
        a = percorso[i + 1]                            #        a  = 3
        totale = totale + km[da][a]                    # 6,4 + 4,8 + 6,8
    return totale                                      # 18,0 km


def minuti_percorso(percorso, minuti, tempo_scarico):
    """
    Calcola la durata del giro in minuti:
        tempo di guida (somma delle tratte) + tempo di scarico per ogni cliente.

    I clienti sono tutti i nodi del percorso tranne il primo e l'ultimo
    (che sono il deposito), quindi sono len(percorso) - 2.
    """
    guida = 0
    for i in range(len(percorso) - 1):
        guida = guida + minuti[percorso[i]][percorso[i + 1]]   # 13 + 10 + 13 = 36
    numero_clienti = len(percorso) - 2                 # [0, 3, 4, 0]: 4 - 2 = 2 clienti
    return guida + numero_clienti * tempo_scarico      # 36 + 2 x 10 = 56 minuti


def carico_percorso(percorso, domande):
    """
    Somma le cassette da consegnare ai clienti del percorso.
    Il deposito non ha domanda, quindi lo salto.
    """
    totale = 0
    for nodo in percorso:                              # 0, 3, 4, 0
        if nodo != ID_DEPOSITO:                        # salto i due 0
            totale = totale + domande[nodo]            # 4 (Golasecca) + 13 (Vergiate)
    return totale                                      # 17 cassette


def orari_arrivo(percorso, minuti, tempo_scarico):
    """
    Calcola dopo quanti minuti dalla partenza il furgone arriva da ogni
    cliente del percorso. E' il tempo che la merce (per esempio i mirtilli
    appena raccolti) passa nel furgone prima di essere consegnata.

    Esempio con percorso [0, 3, 4, 0], 13 minuti da 0 a 3, 10 da 3 a 4 e
    10 minuti di scarico:
        cliente 3: arrivo dopo 13 minuti;
        cliente 4: arrivo dopo 13 + 10 (scarico) + 10 = 33 minuti.

    Restituisce un dizionario { id_cliente: minuti_all_arrivo }.
    """
    arrivi = {}
    tempo = 0                                          # orologio: minuti dalla partenza
    for i in range(len(percorso) - 1):
        da = percorso[i]
        a = percorso[i + 1]
        tempo = tempo + minuti[da][a]                  # guido fino al nodo "a"
        if a != ID_DEPOSITO:                           # il ritorno al deposito non e' un arrivo da un cliente
            arrivi[a] = tempo                          # 3 -> 13; poi 4 -> 33
            tempo = tempo + tempo_scarico   # tempo per scaricare dal cliente
    return arrivi                                      # {3: 13, 4: 33}


def valore_percorso(percorso, istanza):
    """
    Restituisce il valore da RENDERE MINIMO per un percorso, in base al
    criterio scelto in parametri.json ("criterio_ottimizzazione"):
      - "km":     i chilometri del giro;
      - "minuti": la durata del giro (guida + scarichi).

    Perche' serve la scelta: Google Maps propone il percorso piu' VELOCE,
    non il piu' corto. Su alcune tratte la strada piu' veloce e' piu'
    lunga in km (per esempio passa dalla superstrada). Ottimizzare i
    minuti e' quindi coerente con il modo in cui sono stati rilevati i dati.
    """
    if istanza["criterio"] == "km":
        return km_percorso(percorso, istanza["km"])    # sarebbe 18,0
    else:
        return minuti_percorso(percorso, istanza["minuti"], istanza["tempo_scarico"])   # oggi: 56


def descrivi_percorso(percorso, nodi):
    """Trasforma un percorso in una stringa leggibile con i nomi dei comuni."""
    nomi = [nodi[nodo]["comune"] for nodo in percorso]   # ["Somma Lombardo", "Golasecca", "Vergiate", "Somma Lombardo"]
    return " -> ".join(nomi)                           # "Somma Lombardo -> Golasecca -> Vergiate -> Somma Lombardo"

