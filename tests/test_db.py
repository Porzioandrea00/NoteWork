import re
import sqlite3

from src.database.db import Gestore_DB


def test_crea_la_tabella_note(db):
    connection = sqlite3.connect(db.db_path)
    columns = [row[1] for row in connection.execute("PRAGMA table_info(note)")]
    connection.close()

    assert columns == ["id", "title", "content", "created_at", "last_modified_at", "ia_output"]


def test_new_note_salva_la_nota_e_restituisce_l_id(db):
    note_id = db.new_note(title="Riunione", content="Punti da discutere", ia_output="Ticket")

    note = db.get_note_by_id(note_id)

    assert note[0] == note_id
    assert note[1] == "Riunione"
    assert note[2] == "Punti da discutere"
    assert note[5] == "Ticket"


def test_new_note_usa_i_valori_predefiniti(db):
    note = db.get_note_by_id(db.new_note())

    assert note[1] == "Nuova nota"
    assert note[2] == ""
    assert note[5] == ""


def test_la_data_di_creazione_viene_impostata_automaticamente(db):
    note = db.get_note_by_id(db.new_note())

    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", note[3])


def test_get_all_notes_restituisce_tutte_le_note_in_ordine(db):
    first = db.new_note(title="Prima")
    second = db.new_note(title="Seconda")

    notes = db.get_all_notes()

    assert [(n[0], n[1]) for n in notes] == [(first, "Prima"), (second, "Seconda")]


def test_get_all_notes_con_database_vuoto(db):
    assert db.get_all_notes() == []


def test_get_note_by_id_inesistente_restituisce_none(db):
    assert db.get_note_by_id(999) is None


def test_update_note_modifica_tutti_i_campi(db):
    note_id = db.new_note(title="Bozza", content="testo")

    db.update_note(note_id, "Definitiva", "testo nuovo", "2026-10-25 18:00:00", "risposta IA")

    note = db.get_note_by_id(note_id)
    assert note[1:] == ("Definitiva", "testo nuovo", note[3], "2026-10-25 18:00:00", "risposta IA")


def test_update_note_non_tocca_le_altre_note(db):
    note_id = db.new_note(title="Da modificare")
    other_id = db.new_note(title="Da lasciare")

    db.update_note(note_id, "Modificata", "", "", "")

    assert db.get_note_by_id(other_id)[1] == "Da lasciare"


def test_delete_note_elimina_solo_la_nota_indicata(db):
    note_id = db.new_note(title="Da eliminare")
    other_id = db.new_note(title="Da tenere")

    db.delete_note(note_id)

    assert db.get_note_by_id(note_id) is None
    assert db.get_note_by_id(other_id) is not None


def test_le_note_restano_salvate_riaprendo_il_database(tmp_path):
    db_path = tmp_path / "test.db"
    note_id = Gestore_DB(db_path=db_path).new_note(title="Persistente")

    reopened = Gestore_DB(db_path=db_path)

    assert reopened.get_note_by_id(note_id)[1] == "Persistente"
