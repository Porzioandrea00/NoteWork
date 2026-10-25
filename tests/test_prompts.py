import json
from pathlib import Path

PROMPTS_PATH = Path(__file__).resolve().parent.parent / "assets" / "prompts.json"


def test_prompts_json_contiene_i_tre_tipi_di_richiesta():
    prompts = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))

    assert set(prompts) == {"prompt", "ticket", "script"}


def test_nessun_prompt_di_sistema_e_vuoto():
    prompts = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))

    assert all(isinstance(text, str) and text.strip() for text in prompts.values())
