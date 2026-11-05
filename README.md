# PW23 – Pianificazione delle consegne di un'impresa agroalimentare

Project work, CdS Informatica per le Aziende Digitali (L-31), Università Telematica Pegaso.
Traccia PW 23: confronto tra un veicolo (TSP) e due veicoli (CVRP),
risolti per enumerazione completa in Python, con pagina HTML dei risultati.

Progetto in corso di sviluppo.

## Dati (cartella `data/`)

- `nodi.csv`: il deposito (Somma Lombardo) e i cinque clienti, uno per ciascun
  comune confinante (matrice di contiguità ISTAT 2025), con gli abitanti
  ISTAT al 1/1/2025. Le coordinate servono solo per disegnare il grafo.
- `distanze.csv`: km e minuti delle 30 tratte, rilevati a mano su Google Maps
  il 03/11/2026 al mattino (primo percorso proposto, in auto). Ogni tratta è
  rilevata nei due sensi perché le distanze stradali possono essere diverse
  (matrice asimmetrica).
- `parametri.json`: cassette del giro, capacità dei furgoni, tempo di scarico,
  prezzi (noleggio, gasolio, autista) e intervalli dell'analisi di sensibilità.
  Il campo `nota` riassume l'origine di ogni valore.
- `rilevazione/verifica_istat_distanze.csv`: confronto tra le distanze di
  Google Maps e la matrice ufficiale ISTAT delle distanze tra comuni
  (`minuti_istat_TEP` = tempo effettivo di percorrenza, con traffico).
  È letto da `src/verifica_distanze.py`, che ne calcola il riepilogo.

Le fonti complete, con link e data di consultazione, sono nel rapporto.

## Codice (cartella `src/`)

Solo Python 3 con la libreria standard.

- `domande.py`: ripartisce le cassette del giro tra i clienti in proporzione
  agli abitanti, con il metodo dei resti più grandi (risultato: 7, 9, 4, 13, 22).
- `istanza.py`: legge i file di `data/` in un unico dizionario e controlla che
  i dati siano completi e rispettino le condizioni della traccia (un veicolo
  grande basta per tutta la domanda, uno piccolo no).
- `verifica_distanze.py`: confronta le distanze rilevate con la matrice ISTAT,
  separando le tratte tra clienti da quelle con il deposito.
- `percorsi.py`: funzioni comuni ai due scenari per calcolare km, minuti,
  carico e orari di arrivo di un giro.

## Test (cartella `tests/`)

Test automatici con il modulo `unittest` della libreria standard, un file
per modulo. Per ora c'è `test_domande.py`, che controlla la ripartizione
delle cassette. Si eseguono dalla cartella principale con:

```
python3 -m unittest discover tests
```
