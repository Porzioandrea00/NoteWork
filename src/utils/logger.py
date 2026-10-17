import logging
import time

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
logs_path = BASE_DIR / "app.log"

logging.basicConfig(
    filename=logs_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def time_tracker(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        
        execution_time = round(end - start, 2)
        prompt = args[1] if len(args) > 1 else "Nessun prompt fornito"
        
        log_message = f"Metodo: {func.__name__} | Tempo: {execution_time}s | Prompt: ({prompt}) | Risposta: {result}"
        logging.info(log_message)
        
        return result
    return wrapper