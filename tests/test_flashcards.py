"""Tests for the flashcards program: normal cases, limits, and bad input."""

import pytest

from cards.models import Card, Deck
from cards.quiz import QuizSession
from cards.storage import load_decks, save_decks

# ---------- Card ----------

def test_card_strips_extra_spaces():
    card = Card(" hello ", " world ")
    assert card.front == "hello"
    assert card.back == "world"



def test_card_with_empty_text_is_rejected():
    with pytest.raises(ValueError):
        Card("   ", "answer")


def test_card_check_ignores_case_and_spaces():
    card =Card("Capital of Thailand?", "Bangkok")
    assert card.check("  bangkok ")
    assert not card.check("Chiang Mai")


# ---------- Deck ----------

def test_deck_add_card_and_known_count():
    deck = Deck("Words")
    first = deck.add_card("a", "1") 
    deck.add_card("b", "2")
    first.known = True
    assert len(deck.cards) == 2
    assert deck.known_count == 1



def test_remove_card_with_bad_position_raises():
    deck =Deck("Words")
    deck.add_card("a", "1")
    with pytest.raises(IndexError):
        deck.remove_card(5)


def test_due_cards_skips_known_cards():
    deck = Deck("Words")
    known = deck.add_card("a", "1")
    deck.add_card("b", "2")
    known.known = True
    due = list(deck.due_cards())
    assert [card.front for card in due] == ["b"]


# ---------- QuizSession ----------

def test_correct_answer_marks_card_known_and_scores():
    deck = Deck("Words")
    card = deck.add_card("a", "1")
    session = QuizSession(deck)
    assert session.answer(card, "1") is True
    assert card.known
    assert session.correct == 1
    assert session.score_percent == 100


def test_wrong_answer_keeps_card_unknown():
    deck = Deck("Words")
    card = deck.add_card("a", "1")
    session = QuizSession(deck)
    assert session.answer(card, "wrong") is False
    assert not card.known
    assert session.score_percent == 0


def test_score_is_zero_when_nothing_was_asked():
    session = QuizSession(Deck("Empty"))
    assert session.score_percent == 0.0

 # ---------- Storage ----------

def test_save_then_load_gives_same_decks(tmp_path):
    path = tmp_path / "decks.json"
    deck = Deck("Words")
    card = deck.add_card("a", "1")
    card.known = True
    assert save_decks([deck], path) is True
    loaded = load_decks(path)
    assert len(loaded) == 1
    assert loaded[0].name == "Words"
    assert loaded[0].cards[0].known is True


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_decks(tmp_path / "nothing.json") == []


def test_load_broken_json_does_not_crash(tmp_path):
    path = tmp_path / "decks.json"
    path.write_text("{ this is not json", encoding="utf-8")
    assert load_decks(path) == []


def test_load_wrong_format_does_not_crash(tmp_path):
    path = tmp_path / "decks.json"
    path.write_text('[{"title": "no name key"}]', encoding="utf-8")
    assert load_decks(path) == []