import json
from pathlib import Path

import httpx
import pytest
from ollama import ResponseError

from src.controllers.AIAssistant import AIAssistant

PROMPTS = json.loads((Path(__file__).resolve().parent.parent / "assets" / "prompts.json").read_text(encoding="utf-8"))


@pytest.fixture
def assistant():
    return AIAssistant("llama3.2")


def test_chat_restituisce_la_risposta_un_pezzo_alla_volta(assistant, fake_ollama):
    fake_ollama.respond("Ciao", " mondo")

    assert list(assistant.chat("Saluta")) == ["Ciao", " mondo"]


def test_chat_usa_il_modello_scelto_in_streaming(assistant, fake_ollama):
    fake_ollama.respond("ok")

    list(assistant.chat("Saluta"))

    assert fake_ollama.chat_calls[0]["model"] == "llama3.2"
    assert fake_ollama.chat_calls[0]["stream"] is True


def test_chat_salva_la_risposta_completa_nella_cronologia(assistant, fake_ollama):
    fake_ollama.respond("Ciao", " mondo")

    list(assistant.chat("Saluta"))

    assert assistant.messages == [
        {"role": "user", "content": "Saluta"},
        {"role": "assistant", "content": "Ciao mondo"},
    ]


@pytest.mark.parametrize("task_type", ["prompt", "ticket", "script"])
def test_task_type_aggiunge_il_prompt_di_sistema(assistant, fake_ollama, task_type):
    fake_ollama.respond("ok")

    list(assistant.chat("Testo selezionato", task_type=task_type))

    assert fake_ollama.chat_calls[0]["messages"] == [
        {"role": "system", "content": PROMPTS[task_type]},
        {"role": "user", "content": "Testo selezionato"},
    ]


def test_senza_task_type_invia_solo_il_testo(assistant, fake_ollama):
    fake_ollama.respond("ok")

    list(assistant.chat("Testo selezionato"))

    assert fake_ollama.chat_calls[0]["messages"] == [{"role": "user", "content": "Testo selezionato"}]


def test_ogni_richiesta_parte_senza_cronologia(assistant, fake_ollama):
    fake_ollama.respond("prima risposta")
    list(assistant.chat("Prima domanda"))

    fake_ollama.respond("seconda risposta")
    list(assistant.chat("Seconda domanda"))

    assert fake_ollama.chat_calls[1]["messages"] == [{"role": "user", "content": "Seconda domanda"}]


def test_task_type_sconosciuto_non_chiama_ollama(assistant, fake_ollama):
    assert list(assistant.chat("Testo", task_type="inesistente")) == ["Si è verificato un errore sconosciuto."]
    assert fake_ollama.chat_calls == []


def test_connessione_interrotta_durante_la_risposta(assistant, fake_ollama):
    fake_ollama.respond("Ciao", httpx.ReadError("connessione chiusa"))

    output = list(assistant.chat("Saluta"))

    assert output == ["Ciao", "\n[Errore: Connessione interrotta durante la generazione]"]
    assert assistant.messages == []


@pytest.mark.parametrize(
    "error, expected",
    [
        (httpx.ConnectError("Connection refused"), "Impossibile connettersi al server di Ollama. Assicurati che sia avviato."),
        (httpx.ReadTimeout("timed out"), "Il modello ha impiegato troppo tempo a rispondere."),
        (
            ResponseError("context length exceeded", 400),
            "La conversazione è troppo lunga per la memoria del modello. La cronologia è stata resettata.",
        ),
    ],
    ids=["ollama-spento", "timeout", "contesto-troppo-lungo"],
)
def test_errori_di_ollama_mostrano_un_messaggio_chiaro(assistant, fake_ollama, error, expected):
    fake_ollama.respond(error)

    assert list(assistant.chat("Saluta")) == [expected]


def test_modello_non_trovato_viene_scaricato(assistant, fake_ollama):
    fake_ollama.respond(ResponseError("model 'llama3.2' not found", 404))

    output = list(assistant.chat("Saluta"))

    assert output == ["Modello non trovato, scaricato con successo. Riprova."]
    assert fake_ollama.pull_calls == ["llama3.2"]


def test_modello_non_trovato_e_download_fallito(assistant, fake_ollama):
    fake_ollama.respond(ResponseError("model 'llama3.2' not found", 404))
    fake_ollama.pull_error = ResponseError("pull failed", 500)

    assert list(assistant.chat("Saluta")) == ["Modello non trovato e download fallito."]
