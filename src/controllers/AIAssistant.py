import logging
import httpx
import ollama

from ollama import ResponseError
from src.utils.logger import time_tracker

class AIAssistant:
    def __init__(self, modello, messages = None):
        self.modello = modello
        if messages is None:
            self.messages = []
        else:
            self.messages = messages
    
    @time_tracker
    def chat(self, prompt):
        try: 
            
            self.messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model = self.modello,
                messages = self.messages,
                stream = True               # Generatore
            )
            
            response_text = ""
            
            for chunk in response:
                response_text += chunk['message']['content']
                yield chunk["message"]["content"]
            
            # response_text = response['message']['content']
            self.messages.append({"role": "assistant", "content": response_text})
        
        except ResponseError as e:
            print(f"Errore dell'API di Ollama (Codice {e.status_code}): {e.error}")
            self.messages.pop()
            
            if e.status_code == 404:
                logging.error(f"Modello non trovato: {e.error}")
                print("Modello non trovato. Tentativo di download in corso...")
                ollama.download_model(self.modello)
                response_text = "Modello non trovato."
                yield response_text
        
        except ConnectionError:
            logging.error("Impossibile connettersi al server di Ollama.")
            response_text = "Impossibile connettersi al server di Ollama."
            yield response_text
            self.messages.pop()
            
            
        except httpx.TimeoutException:
            logging.error("Timeout durante la richiesta al server di Ollama.")
            response_text = "Il modello ha impiegato troppo tempo a rispondere"
            yield response_text
            self.messages.pop()      
            
        except Exception as e:
            logging.error(f"Tipo errore: {type(e).__name__} | Dettaglio: {e}")
            response_text = "Si è verificato un errore sconosciuto."
            yield response_text
            self.messages.pop()
            
