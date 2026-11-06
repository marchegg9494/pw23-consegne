"""
vrp.py

SCENARIO 2: due veicoli piccoli identici, ognuno con capacita' inferiore
alla domanda totale (50 cassette contro 55): da solo nessuno dei due
basta, quindi servono entrambi.

Il problema e' un Capacitated Vehicle Routing Problem (CVRP, "problema
di instradamento dei veicoli con vincolo di capacita'"): bisogna
decidere QUALI clienti servire con ciascun veicolo e IN CHE ORDINE,
senza superare la capacita' di nessuno dei due. Si cerca la soluzione
con il valore totale minimo (somma dei due giri) secondo il criterio
scelto: minuti o chilometri (vedi "criterio_ottimizzazione" in
parametri.json).

Metodo: ENUMERAZIONE COMPLETA

Idea usata per generare tutte le soluzioni:
prendo ogni possibile ordine dei 5 clienti (le 120 permutazioni, come
nel TSP) e lo "taglio" in due pezzi. Il primo pezzo e' il giro del
veicolo A, il secondo quello del veicolo B.

Esempio con la permutazione (3, 4, 1, 2, 5):
    taglio dopo 1 cliente  -> A: 3           B: 4, 1, 2, 5
    taglio dopo 2 clienti  -> A: 3, 4        B: 1, 2, 5
    taglio dopo 3 clienti  -> A: 3, 4, 1     B: 2, 5
    taglio dopo 4 clienti  -> A: 3, 4, 1, 2  B: 5
Non taglio mai prima del primo o dopo l'ultimo cliente, perche' un
veicolo resterebbe vuoto (e la traccia chiede di usarli entrambi).

Con 5 clienti: 120 permutazioni x 4 tagli = 480 soluzioni generate.
In questo modo ottengo tutte le ripartizioni possibili dei clienti
tra i due veicoli e, per ognuna, tutti gli ordini di visita.

Nota: siccome i due veicoli sono identici, la soluzione "A fa 3-4,
B fa 1-2-5" e la soluzione "A fa 1-2-5, B fa 3-4" sono in pratica la
stessa. Le genero comunque tutte e due: il risultato ottimo non cambia
e il codice resta piu' semplice. Le soluzioni davvero diverse sono
quindi la meta' di quelle ammissibili (432 / 2 = 216) scartando le soluzioni non valide.

Complessita': n! permutazioni x (n - 1) tagli, e ogni soluzione si
valuta sommando le sue tratte, quindi il tempo cresce come n^2 x n!.
Come nel TSP, permutations() produce un ordine alla volta: in memoria
restano solo la soluzione in esame e la migliore trovata finora.
"""

from itertools import permutations   # genera tutti gli ordinamenti possibili di una lista

from percorsi import crea_percorso, km_percorso, minuti_percorso, carico_percorso, valore_percorso, orari_arrivo


def risolvi_vrp_due_veicoli(istanza):
    """
    Genera tutte le soluzioni con due veicoli, scarta quelle che non
    rispettano la capacita' e restituisce la migliore.

    Restituisce un dizionario con:
      - veicoli: lista di due dizionari (uno per veicolo) con percorso,
                 km, minuti, carico e arrivi
      - km: chilometri totali (somma dei due giri)
      - minuti_totali: somma delle durate dei due giri
      - minuti_giro_piu_lungo: durata del giro piu' lungo, cioe' dopo
        quanto tempo sono finite tutte le consegne (i due veicoli
        partono insieme e viaggiano in contemporanea)
      - soluzioni_generate, soluzioni_scartate, soluzioni_ammissibili

    Esempio con i dati del progetto: 480 generate, 48 scartate,
    432 ammissibili; migliore A = [0, 1, 2, 5, 0] (71 min, 38 cassette)
    e B = [0, 3, 4, 0] (56 min, 17 cassette).
    """
    clienti = istanza["clienti"]                       # [1, 2, 3, 4, 5]
    km = istanza["km"]
    domande = istanza["domande"]                       # {1: 7, 2: 9, 3: 4, 4: 13, 5: 22}
    capacita = istanza["capacita_piccolo"]             # 50 cassette per furgone

    migliore = None          # (giro_a, giro_b) della soluzione migliore; None = "non ancora trovata"
    miglior_valore = None
    generate = 0             # alla fine 480
    scartate = 0             # alla fine 48
    ammissibili = 0          # alla fine 432

    for sequenza in permutations(clienti):             # 120 ordini, come nel TSP
        # Il taglio va da 1 a (numero clienti - 1), cioe' 1, 2, 3, 4:
        # cosi' ogni veicolo ha almeno un cliente.
        for taglio in range(1, len(clienti)):
            generate = generate + 1

            # sequenza[:taglio] = i clienti prima del taglio, sequenza[taglio:] = quelli dopo.
            # Con (3, 4, 1, 2, 5) e taglio 2: (3, 4) e (1, 2, 5).
            giro_a = crea_percorso(sequenza[:taglio])   # [0, 3, 4, 0]
            giro_b = crea_percorso(sequenza[taglio:])   # [0, 1, 2, 5, 0]

            # VERIFICA DEL VINCOLO DI CAPACITA':
            # se anche uno solo dei due veicoli e' troppo carico, la
            # soluzione non e' ammissibile e la scarto.
            # Esempio: A con il solo cliente 3 (4 cassette) lascia a B
            # 7 + 9 + 13 + 22 = 51 cassette, una in piu' di 50: scartata.
            if carico_percorso(giro_a, domande) > capacita or carico_percorso(giro_b, domande) > capacita:
                scartate = scartate + 1
                continue   # passo alla prossima soluzione

            ammissibili = ammissibili + 1
            # Il valore della soluzione e' la somma dei due giri: con il
            # criterio "minuti" conta il lavoro totale dei due autisti,
            # che e' anche quello che si paga.
            valore = valore_percorso(giro_a, istanza) + valore_percorso(giro_b, istanza)

            if miglior_valore is None or valore < miglior_valore:
                miglior_valore = valore                # alla fine: 71 + 56 = 127 minuti
                migliore = (giro_a, giro_b)

    # Se non c'e' nessuna soluzione ammissibile mi fermo con un messaggio.
    # Con i controlli di istanza.py non dovrebbe succedere, ma e' meglio
    # fermarsi con una spiegazione che proseguire con migliore = None.
    if migliore is None:
        raise ValueError("Nessuna soluzione con due veicoli rispetta la capacita'.")

    # Preparo i dettagli dei due giri della soluzione migliore.
    veicoli = []
    for giro in migliore:
        veicoli.append({
            "percorso": giro,
            "km": round(km_percorso(giro, km), 1),                                              # 24.1 e 18.0
            "minuti": round(minuti_percorso(giro, istanza["minuti"], istanza["tempo_scarico"])),  # 71 e 56
            "carico": carico_percorso(giro, domande),                                           # 38 e 17
            "arrivi": orari_arrivo(giro, istanza["minuti"], istanza["tempo_scarico"]),
        })

    risultato = {
        "veicoli": veicoli,
        "km": round(veicoli[0]["km"] + veicoli[1]["km"], 1),                       # 42.1
        "minuti_totali": veicoli[0]["minuti"] + veicoli[1]["minuti"],              # 127
        "minuti_giro_piu_lungo": max(veicoli[0]["minuti"], veicoli[1]["minuti"]),  # 71
        "soluzioni_generate": generate,                                            # 480
        "soluzioni_scartate": scartate,                                            # 48
        "soluzioni_ammissibili": ammissibili,                                      # 432
    }
    return risultato
