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
  È letto da `src/verifica_distanze.py`, che riassume il confronto nella pagina.

Le fonti complete, con link e data di consultazione, sono nel rapporto.
