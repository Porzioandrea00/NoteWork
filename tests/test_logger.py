import logging

from src.utils.logger import time_tracker


class Servizio:
    @time_tracker
    def esegui(self, prompt):
        return f"risposta a {prompt}"

    @time_tracker
    def senza_prompt(self):
        return "fatto"


def test_time_tracker_restituisce_il_risultato_della_funzione():
    assert Servizio().esegui("ciao") == "risposta a ciao"


def test_time_tracker_registra_metodo_prompt_e_risposta(caplog):
    caplog.set_level(logging.INFO)

    Servizio().esegui("ciao")

    assert "Metodo: esegui" in caplog.text
    assert "Prompt: (ciao)" in caplog.text
    assert "Risposta: risposta a ciao" in caplog.text


def test_time_tracker_senza_prompt(caplog):
    caplog.set_level(logging.INFO)

    Servizio().senza_prompt()

    assert "Prompt: (Nessun prompt fornito)" in caplog.text
