# NoteWork

![Python 3.13](https://img.shields.io/badge/python-3.13-blue)
![Licenza MIT](https://img.shields.io/badge/licenza-MIT-green)
![Test con pytest](https://img.shields.io/badge/test-pytest-orange)

Applicazione desktop per prendere appunti di lavoro, con un assistente IA locale che trasforma il testo selezionato in un ticket di sviluppo, in un prompt per generare immagini di interfacce o in uno script Python.

L'interfaccia è realizzata con **CustomTkinter**, le note sono salvate in un database **SQLite** locale e l'IA gira in locale tramite **Ollama** (modello predefinito: `llama3.2`). Nessun testo viene inviato a servizi esterni.

## Screenshot

<!-- Aggiungi le immagini nella cartella docs/ con questi nomi: screenshot.png e demo.gif -->
![NoteWork: elenco delle note, editor e risposta dell'IA](docs/screenshot.png)

![Demo: dal testo selezionato al ticket generato dall'IA](docs/demo.gif)

## Funzionalità

- **Gestione note**: crea, apri, modifica, salva ed elimina le note. L'elenco è nella barra laterale sinistra; un clic sul titolo apre la nota.
- **Assistente IA** (barra laterale destra). Lavora sul testo selezionato nell'editor:
  - **IA Ticket**: trasforma il testo in un ticket di sviluppo Agile con le sezioni *Titolo Ticket*, *User Story*, *Descrizione e Contesto Tecnico* e *Criteri di Accettazione*.
  - **IA Prompt**: traduce i requisiti in un prompt in inglese per le IA generative di immagini (Midjourney, DALL-E) che descrive layout, stile e composizione dell'interfaccia.
  - **IA Script**: genera codice Python con type hinting, gestione degli errori e commenti.
- **Risposta in streaming**: il testo generato compare man mano nel pannello in basso. Durante l'elaborazione i pulsanti vengono disabilitati per evitare chiamate sovrapposte, la generazione è eseguita in thread separati per non bloccare l'interfaccia.
- **Risultato salvato con la nota**: l'output dell'IA viene salvato insieme alla nota e ricaricato quando la riapri.
- **Esporta**: salva l'output dell'IA in un file `.txt`.

## Requisiti

- Python 3 (sviluppato con Python 3.13)
- [Ollama](https://ollama.com) installato e in esecuzione
- Modello `llama3.2` (o altro modello preferito)

## Installazione

```bash
git clone https://github.com/Porzioandrea00/NoteWork.git
cd NoteWork
python -m venv .venv
.venv\Scripts\activate      # Su Windows
# source .venv/bin/activate # Su macOS/Linux
pip install -r requirements.txt
ollama pull llama3.2
```

## Avvio

```bash
python main.py
```

I percorsi di `NoteWork.db`, `app.log` e `assets/prompts.json` sono calcolati a partire dalla cartella del progetto, quindi l'app si può avviare anche da un'altra cartella (ad esempio `python NoteWork/main.py`). Al primo avvio il database viene creato automaticamente.

## Come si usa

1. Clicca **Nuova nota**: l'editor si attiva con una nota intitolata "Nuova nota".
2. Scrivi il titolo nel campo in alto e il testo nell'editor.
3. Seleziona la parte di testo da elaborare e clicca **IA Ticket**, **IA Prompt** o **IA Script**.
4. Il risultato compare nel pannello in basso. Con **esporta** lo salvi in un file `.txt`.
5. Clicca **salva** per salvare titolo, testo e risultato dell'IA. Il salvataggio non è automatico.
6. Per eliminare la nota aperta clicca **Elimina nota**.

## Struttura del progetto

```
NoteWork/
├── main.py                    # Interfaccia grafica (CustomTkinter) e avvio dell'app
├── requirements.txt           # Dipendenze Python (customtkinter, ollama, httpx)
├── requirements-dev.txt       # Dipendenze per i test (pytest)
├── pytest.ini                 # Configurazione di pytest
├── LICENSE                    # Licenza MIT
├── assets/
│   └── prompts.json           # Prompt di sistema per IA Prompt, IA Ticket e IA Script
├── docs/                      # Screenshot e GIF usati nel README
├── src/
│   ├── controllers/
│   │   └── AIAssistant.py     # Chiamate a Ollama in streaming e gestione degli errori
│   ├── database/
│   │   └── db.py              # Gestore_DB: creazione, lettura, modifica ed eliminazione delle note
│   └── utils/
│       └── logger.py          # Configurazione del log su app.log e decoratore time_tracker
├── tests/
│   ├── conftest.py            # Database temporaneo e Ollama simulato per i test
│   ├── test_ai_assistant.py   # Test dell'assistente IA
│   ├── test_db.py             # Test del database
│   ├── test_logger.py         # Test del decoratore time_tracker
│   └── test_prompts.py        # Test di assets/prompts.json
├── NoteWork.db                # Database SQLite delle note (creato al primo avvio)
└── app.log                    # Log dell'applicazione (creato al primo avvio)
```

## Personalizzazione

- **Modello**: in `main.py` sostituisci `llama3.2` in `AIAssistant('llama3.2')` con un altro modello installato in Ollama, ad esempio `AIAssistant('mistral')`.
- **Prompt**: modifica i testi in `assets/prompts.json` per cambiare il comportamento dei tre pulsanti. Le chiavi `prompt`, `ticket` e `script` devono restare invariate; per aggiungere un nuovo tipo serve anche un pulsante in `main.py`.

## Database

Le note sono salvate nella tabella `note` di `NoteWork.db`:

| Campo              | Tipo     | Contenuto                         |
|--------------------|----------|-----------------------------------|
| `id`               | INTEGER  | Chiave primaria autoincrementale  |
| `title`            | TEXT     | Titolo della nota                 |
| `content`          | TEXT     | Testo della nota                  |
| `created_at`       | DATETIME | Data di creazione                 |
| `last_modified_at` | DATETIME | Data dell'ultimo salvataggio      |
| `ia_output`        | TEXT     | Ultimo risultato dell'IA          |

## Gestione degli errori

- **Ollama non raggiungibile**: nel pannello compare "Impossibile connettersi al server di Ollama. Assicurati che sia avviato."
- **Modello non installato**: l'app scarica il modello con `ollama pull` (circa 2 GB per `llama3.2`, può richiedere qualche minuto) e poi chiede di ripetere la richiesta. Se il download non riesce compare "Modello non trovato e download fallito."
- **Timeout**: compare "Il modello ha impiegato troppo tempo a rispondere."
- **Testo troppo lungo per il modello**: compare "La conversazione è troppo lunga per la memoria del modello. La cronologia è stata resettata."
- **Connessione interrotta mentre arriva la risposta**: il testo già ricevuto resta nel pannello, seguito da "[Errore: Connessione interrotta durante la generazione]".
- **Nessun testo selezionato**: in console viene segnalato l'errore e i pulsanti vengono riabilitati senza blocchi.

Con lo streaming attivo la libreria `ollama` segnala gli errori solo mentre arriva la risposta: `AIAssistant.chat` li intercetta in quel punto e mostra per ciascuno il messaggio corrispondente.

## Test

I test usano **pytest** e non richiedono né Ollama né l'interfaccia grafica: le chiamate a Ollama sono simulate e il database è un file temporaneo, quindi non toccano le tue note né `app.log`.

```bash
pip install -r requirements-dev.txt
pytest
```

| File                         | Cosa verifica                                                                                          |
|------------------------------|--------------------------------------------------------------------------------------------------------|
| `tests/test_db.py`           | Creazione della tabella; inserimento, lettura, modifica ed eliminazione delle note; data di creazione |
| `tests/test_ai_assistant.py` | Risposta in streaming, prompt di sistema di IA Prompt, IA Ticket e IA Script, cronologia, ogni errore di Ollama elencato sopra |
| `tests/test_prompts.py`      | `assets/prompts.json` contiene i tre prompt e nessuno è vuoto                                          |
| `tests/test_logger.py`       | Il decoratore `time_tracker` restituisce il risultato e registra metodo, prompt e risposta            |

L'interfaccia grafica (`main.py`) non è coperta dai test.

## Note

- L'app è **cross-platform** (Windows, macOS, Linux): la gestione del ridimensionamento della finestra adatta lo stato massimizzato al sistema operativo in uso.
- **esporta** salva solo il risultato dell'IA, non il testo della nota.
- Ogni richiesta all'IA è indipendente: l'assistente non mantiene memoria delle conversazioni precedenti.

## Tecnologie

- Python
- CustomTkinter
- SQLite (`sqlite3`)
- Ollama (`llama3.2`)
- pytest

## Licenza

Distribuito con licenza MIT: vedi il file [LICENSE](LICENSE).