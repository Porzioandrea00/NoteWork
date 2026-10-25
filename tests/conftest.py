import logging

import pytest

# I test non devono scrivere in app.log: se il logger principale ha già un
# handler, logging.basicConfig in src/utils/logger.py non fa nulla
logging.getLogger().addHandler(logging.NullHandler())

import src.controllers.AIAssistant as ai_module
from src.database.db import Gestore_DB


@pytest.fixture
def db(tmp_path):
    return Gestore_DB(db_path=tmp_path / "test.db")


class FakeOllama:
    """Sostituisce il client di Ollama: nessuna richiesta parte davvero."""

    def __init__(self):
        self.chat_calls = []
        self.pull_calls = []
        self.pull_error = None
        self.events = []

    def respond(self, *events):
        # Ogni evento è un pezzo di testo da restituire o un'eccezione da sollevare
        self.events = list(events)

    def chat(self, model, messages, stream=False):
        self.chat_calls.append({"model": model, "messages": [dict(m) for m in messages], "stream": stream})
        events = list(self.events)

        def stream_chunks():
            # Come la libreria reale con stream=True: la richiesta parte solo
            # quando si legge la risposta, quindi anche gli errori arrivano qui
            for event in events:
                if isinstance(event, BaseException):
                    raise event
                yield {"message": {"role": "assistant", "content": event}}

        return stream_chunks()

    def pull(self, model):
        self.pull_calls.append(model)
        if self.pull_error:
            raise self.pull_error


@pytest.fixture
def fake_ollama(monkeypatch):
    fake = FakeOllama()
    monkeypatch.setattr(ai_module.ollama, "chat", fake.chat)
    monkeypatch.setattr(ai_module.ollama, "pull", fake.pull)
    return fake
