import time
import logging

logging.basicConfig(
    filename='app.log',                                     # Nome file
    level=logging.INFO,                                     # Livello di log da registratre
    format='%(asctime)s - %(levelname)s - %(message)s',     # Formato
    datefmt='%Y-%m-%d %H:%M:%S'
)

def time_tracker(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs) # Elaborazione risposta IA
        end = time.time()
        
        execution_time = round(end - start, 2) # Arrotondamento a due decimali
                
        # Intercettamento input
        prompt = args[1] if len(args) > 1 else "Nessun prompt fornito"
        
        # Salvataggio nel file
        log_message = f"Metodo: {func.__name__} | Tempo: {execution_time}s | Prompt: ({prompt}) | Risposta: {result}"
        logging.info(log_message)
        
        return result
    return wrapper