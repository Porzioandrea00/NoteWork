# NoteWork

Applicazione desktop per prendere appunti di lavoro, con un assistente IA locale che trasforma il testo selezionato in un ticket di sviluppo, in un prompt per generare immagini di interfacce o in uno script Python.

L'interfaccia è realizzata con **CustomTkinter**, le note sono salvate in un database **SQLite** locale e l'IA gira in locale tramite **Ollama** (modello predefinito: `llama3.2`). Nessun testo viene inviato a servizi esterni.

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

Avvia l'app dalla cartella principale del progetto: i percorsi di `NoteWork.db` e `assets/prompts.json` sono relativi alla cartella corrente. Al primo avvio il database viene creato automaticamente.

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
├── assets/
│   └── prompts.json           # Prompt di sistema per IA Prompt, IA Ticket e IA Script
├── src/
│   ├── controllers/
│   │   └── AIAssistant.py     # Chiamate a Ollama in streaming e gestione degli errori
│   ├── database/
│   │   └── db.py              # Gestore_DB: creazione, lettura, modifica ed eliminazione delle note
│   └── utils/
│       └── logger.py          # Configurazione del log su app.log e decoratore time_tracker
└── NoteWork.db                # Database SQLite delle note
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

- **Ollama non raggiungibile**: nel pannello compare "Impossibile connettersi al server di Ollama." Avvia Ollama e riprova.
- **Modello non installato**: l'app tenta di avvisare o scaricare il modello. Se non presente, l'errore viene mostrato nel pannello IA.
- **Timeout**: compare "Il modello ha impiegato troppo tempo a rispondere".
- **Nessun testo selezionato**: in console viene segnalato l'errore e i pulsanti vengono riabilitati senza blocchi.

## Note

- L'app è **cross-platform** (Windows, macOS, Linux): la gestione del ridimensionamento della finestra adatta lo stato massimizzato al sistema operativo in uso.
- **esporta** salva solo il risultato dell'IA, non il testo della nota.
- Ogni richiesta all'IA è indipendente: l'assistente non mantiene memoria delle conversazioni precedenti.

## Tecnologie

- Python
- CustomTkinter
- SQLite (`sqlite3`)
- Ollama (`llama3.2`)