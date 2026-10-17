import json
import logging
from pathlib import Path
import httpx
import ollama
from ollama import ResponseError
from src.utils.logger import time_tracker


class AIAssistant:

  def __init__(self, modello, messages=None):
    self.modello = modello
    if messages is None:
      self.messages = []
    else:
      self.messages = messages

  @time_tracker
  def chat(self, prompt, task_type=None):
    try:
      self.messages.clear()
      if task_type != None:
        base_dir = Path(__file__).resolve().parent.parent.parent
        prompts_path = base_dir / "assets/prompts.json"

        with open(prompts_path, "r", encoding="utf-8") as f:
          prompts_dict = json.load(f)
          prompt_type = prompts_dict[task_type]
          self.messages.append({"role": "system", "content": prompt_type})

      self.messages.append({"role": "user", "content": prompt})

      try:
        response = ollama.chat(
            model=self.modello, messages=self.messages, stream=True
        )
      except Exception as conn_init_err:
        raise ConnectionError(
            "Impossibile connettersi a Ollama"
        ) from conn_init_err

      response_text = ""

      try:
        for chunk in response:
          content = chunk.get("message", {}).get("content", "")
          response_text += content
          yield content
      except Exception as stream_err:
        logging.error(f"Errore durante lo streaming dei chunk: {stream_err}")
        yield "\n[Errore: Connessione interrotta durante la generazione]"
        if self.messages:
          self.messages.pop()
        return

      self.messages.append({"role": "assistant", "content": response_text})

    except ResponseError as e:
      print(f"Errore dell'API di Ollama (Codice {e.status_code}): {e.error}")
      if self.messages:
        self.messages.pop()

      if e.status_code == 404:
        logging.error(f"Modello non trovato: {e.error}")
        print("Modello non trovato. Tentativo di download in corso...")
        try:
          ollama.pull(self.modello)
          yield "Modello non trovato, scaricato con successo. Riprova."
        except Exception as pull_err:
          logging.error(f"Errore durante il download del modello: {pull_err}")
          yield "Modello non trovato e download fallito."
      elif e.status_code == 400 and (
          "context" in str(e.error).lower() or "length" in str(e.error).lower()
      ):
        logging.error(
            f"Superata la finestra di contesto del modello: {e.error}"
        )
        yield "La conversazione è troppo lunga per la memoria del modello. La cronologia è stata resettata."
        self.messages.clear()
      else:
        logging.error(f"Errore Ollama [{e.status_code}]: {e.error}")
        yield f"Errore del server Ollama: {e.error}"

    except ConnectionError:
      logging.error("Impossibile connettersi al server di Ollama.")
      yield "Impossibile connettersi al server di Ollama. Assicurati che sia avviato."
      if self.messages:
        self.messages.pop()

    except httpx.TimeoutException:
      logging.error("Timeout durante la richiesta al server di Ollama.")
      yield "Il modello ha impiegato troppo tempo a rispondere."
      if self.messages:
        self.messages.pop()

    except Exception as e:
      logging.error(f"Tipo errore: {type(e).__name__} | Dettaglio: {e}")
      yield "Si è verificato un errore sconosciuto."
      if self.messages:
        self.messages.pop()