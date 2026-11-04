"""
istanza.py

Questo modulo si occupa di LEGGERE i dati del problema dai file nella
cartella "data" e di CONTROLLARE che siano corretti prima di iniziare
qualsiasi calcolo.

Con "istanza" si intende l'insieme di tutti i dati che descrivono
un caso concreto del problema:
  - i nodi del grafo (il deposito e i clienti);
  - le distanze (in km) e i tempi di percorrenza (in minuti) tra i nodi;
  - la quantita' di merce da consegnare a ogni cliente;
  - le capacita' dei veicoli e gli altri parametri.

I file letti sono:
  - data/nodi.csv        -> elenco dei nodi
  - data/distanze.csv    -> una riga per ogni tratta da un nodo a un altro
  - data/parametri.json  -> cassette totali del giro, capacita' dei veicoli,
                            tempo di scarico

Le cassette da consegnare a ogni cliente NON sono lette da un file:
vengono calcolate da domande.py a partire dagli abitanti dei comuni.

"""

import csv    
import json   
import os     

from domande import calcola_domande   # il modulo del passo 3



ID_DEPOSITO = 0   # sempre id 0 - punto da cui partono e tonrano tutti i veicoli


def leggi_nodi(percorso_file):
    """
    Legge il file dei nodi e restituisce un dizionario
    { id_nodo: {"comune": ..., "ruolo": ..., "abitanti": ..., "lat": ..., "lon": ...} }.

    """
    nodi = {}                                          # si riempie riga per riga
    with open(percorso_file, encoding="utf-8") as f:   # "with" chiude il file da solo alla fine
        lettore = csv.DictReader(f)                    # ogni riga diventa un dizionario con i nomi delle colonne
        for riga in lettore:                           # riga = {"id": "3", "comune": "Golasecca", "abitanti": "2635", ...}
            id_nodo = int(riga["id"])                  # dal CSV arriva testo: "3" -> 3
            if riga["abitanti"] == "":                 # cella vuota: e' il deposito
                abitanti = 0
            else:
                abitanti = int(riga["abitanti"])       
            nodi[id_nodo] = {
                "comune": riga["comune"],
                "ruolo": riga["ruolo"],                # "deposito" oppure "cliente"
                "abitanti": abitanti,
                "lat": float(riga["lat"]),             
                "lon": float(riga["lon"]),
            }
    return nodi                                        # 6 nodi: 0 (deposito) e 1..5 (clienti)


def leggi_distanze(percorso_file):
    """
    Legge il file delle distanze.

    Ogni riga del file descrive UNA tratta in UN senso di marcia
    (per esempio da 0 a 1). La tratta inversa (da 1 a 0) e' su
    un'altra riga, perche' le distanze stradali reali possono essere
    diverse nei due sensi (sensi unici, svincoli, ecc.).
    Si parla quindi di matrice "asimmetrica".

    Restituisce due dizionari "a due livelli":
      km[da][a]      -> chilometri della tratta
      minuti[da][a]  -> minuti di guida della tratta
    
    """
    km = {}
    minuti = {}
    with open(percorso_file, encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        for riga in lettore:                           # riga = {"da": "0", "a": "3", "km": "6.4", "minuti": "13", ...}
            da = int(riga["da"])
            a = int(riga["a"])
            # Se e' la prima tratta che parte da questo nodo, creo il
            # dizionario interno vuoto.
            if da not in km:
                km[da] = {}                            # "riga" vuota della matrice
                minuti[da] = {}
            km[da][a] = float(riga["km"])              # km[0][3] = 6.4
            minuti[da][a] = float(riga["minuti"])      # minuti[0][3] = 13.0
    return km, minuti                                  # due valori restituiti insieme (una "tupla")


def leggi_parametri(percorso_file):
    """Legge il file JSON dei parametri e lo restituisce come dizionario."""
    with open(percorso_file, encoding="utf-8") as f:
        return json.load(f)                            # JSON -> dizionario Python, con numeri gia' convertiti


def controlla_istanza(istanza):
    """
    Controlla che i dati siano coerenti. Se trova un problema si ferma
    con un messaggio chiaro, cosi' non si rischia di calcolare percorsi
    "ottimi" partendo da dati sbagliati.

    I controlli sono di due tipi:
      1) controlli sui dati (manca una distanza? c'e' un valore negativo?);
      2) controlli richiesti dalla traccia del project work sulle quantita':
         - un solo veicolo grande deve bastare per tutti i clienti;
         - un solo veicolo piccolo NON deve bastare (cosi' nello
           scenario 2 servono davvero entrambi i veicoli);
         - due veicoli piccoli insieme devono bastare;
         - nessun cliente deve chiedere piu' di quanto entra in un
           veicolo piccolo (altrimenti non potrebbe essere servito).
    """
    nodi = istanza["nodi"]                             
    km = istanza["km"]
    minuti = istanza["minuti"]
    domande = istanza["domande"]
    q_grande = istanza["capacita_grande"]              # 60
    q_piccolo = istanza["capacita_piccolo"]            # 50

    errori = []                                        # raccolgo TUTTI gli errori, non solo il primo

    # --- 1) Controlli sui dati ---

    # Il deposito deve esistere.
    if ID_DEPOSITO not in nodi:
        errori.append("Nel file dei nodi manca il deposito (id 0).")

    # Per ogni coppia di nodi diversi deve esistere la tratta,
    # con valori positivi.
    for da in nodi:                                    # 6 x 6 = 36 coppie...
        for a in nodi:
            if da == a:                                # ...meno le 6 da un nodo a se stesso = 30 tratte
                continue                               # salta al prossimo "a"
            if da not in km or a not in km[da]:
                errori.append(f"Manca la tratta da {da} a {a} nel file delle distanze.")
            else:
                if km[da][a] <= 0:
                    errori.append(f"La tratta da {da} a {a} ha km non positivi.")
                if minuti[da][a] <= 0:
                    errori.append(f"La tratta da {da} a {a} ha minuti non positivi.")

    # Ogni cliente deve avere abitanti positivi (servono per la domanda)
    # e la domanda calcolata deve essere almeno 1 cassetta.
    for id_nodo, dati in nodi.items():                 # items() da' coppie (chiave, valore)
        if dati["ruolo"] == "cliente":
            if dati["abitanti"] <= 0:
                errori.append(f"Il cliente {id_nodo} non ha il numero di abitanti in nodi.csv.")
            elif domande[id_nodo] <= 0:
                errori.append(
                    f"Al cliente {id_nodo} risultano 0 cassette: il comune e' troppo piccolo "
                    f"rispetto al totale del giro."
                )

    # --- 2) Controlli richiesti dalla traccia ---
    totale = sum(domande.values())                     # 7 + 9 + 4 + 13 + 22 = 55

    if totale > q_grande:                              # 55 > 60? no -> ok
        errori.append(
            f"Il veicolo grande ({q_grande} cassette) non basta per tutta "
            f"la domanda ({totale} cassette)."
        )
    if totale <= q_piccolo:                            # 55 <= 50? no -> ok
        errori.append(
            f"Un solo veicolo piccolo ({q_piccolo} cassette) basta per tutta la "
            f"domanda ({totale}): nello scenario 2 non servirebbero due veicoli."
        )
    if totale > 2 * q_piccolo:                         # 55 > 100? no -> ok
        errori.append(
            f"Due veicoli piccoli ({2 * q_piccolo} cassette in tutto) non bastano "
            f"per la domanda totale ({totale} cassette)."
        )
    for id_cliente, quantita in domande.items():       # il cliente piu' grande e' Cardano: 22
        if quantita > q_piccolo:                       # 22 > 50? no -> ok
            errori.append(
                f"Il cliente {id_cliente} chiede {quantita} cassette, piu' della "
                f"capacita' di un veicolo piccolo ({q_piccolo})."
            )

    # Se ho trovato almeno un errore, li mostro tutti insieme e mi fermo.
    if errori:                                         
        messaggio = "Dati non validi:\n - " + "\n - ".join(errori)   # un errore per riga
        raise ValueError(messaggio)                    # ferma il programma e mostra il messaggio


def carica_istanza(cartella_dati):
    """
    Funzione principale del modulo: legge tutti i file, mette i dati in
    un unico dizionario "istanza", lo controlla e lo restituisce.

    Usare un solo dizionario evita di passare tante variabili diverse
    alle funzioni che risolvono il problema.
    """
    nodi = leggi_nodi(os.path.join(cartella_dati, "nodi.csv"))          # "data" + "nodi.csv" -> "data/nodi.csv"
    km, minuti = leggi_distanze(os.path.join(cartella_dati, "distanze.csv"))   # due variabili in una riga
    parametri = leggi_parametri(os.path.join(cartella_dati, "parametri.json"))

    # Le domande si calcolano dagli abitanti (vedi domande.py).
    domande = calcola_domande(nodi, parametri["cassette_totali_giro"])  # {1: 7, 2: 9, 3: 4, 4: 13, 5: 22}

    # La lista dei clienti serve spesso: la calcolo una volta sola.
    clienti = [id_nodo for id_nodo in nodi if nodi[id_nodo]["ruolo"] == "cliente"]
    clienti.sort()                                     # [1, 2, 3, 4, 5]

    istanza = {
        "nodi": nodi,
        "clienti": clienti,
        "km": km,
        "minuti": minuti,
        "domande": domande,
        "capacita_grande": parametri["capacita_veicolo_grande"],     # 60
        "capacita_piccolo": parametri["capacita_veicolo_piccolo"],   # 50
        "tempo_scarico": parametri["tempo_scarico_minuti"],          # 10
        "criterio": parametri["criterio_ottimizzazione"],            # "minuti"
        "tempo_massimo_consegna": parametri["tempo_massimo_consegna_minuti"],   # 60
        # Prezzi e analisi di sensibilita' non servono per i percorsi:
        # li passo cosi' come sono a costi.py e sensibilita.py.
        "prezzi": parametri["prezzi"],
        "sensibilita": parametri["sensibilita"],
    }

    # Il criterio puo' essere solo "minuti" o "km".
    if istanza["criterio"] not in ("minuti", "km"):
        raise ValueError('In parametri.json "criterio_ottimizzazione" deve essere "minuti" o "km".')

    controlla_istanza(istanza)                         # se i dati sono sbagliati, si ferma qui
    return istanza

