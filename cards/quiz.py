"""Quiz logic: check answers, mark known cards, and keep the score."""

from cards.models import Card, Deck


class QuizSession:
    """One round of quiz on a deck. It only counts and checks; it does not print."""

    def __init__(self, deck: Deck) -> None:
        self.deck = deck
        self.asked = 0
        self.correct = 0

    def __str__(self) -> float:
        """Show the score, for example 'Quiz on Words: 3/4 correct'."""
        return f"Quiz on {self.deck.name}: {self.correct}/{self.asked} correct"

    @property
    def score_percent(self) -> float:
        """Score as a percent (0 if no card was asked yet)."""
        if self.asked == 0:
            return 0.0
        return self.correct / self.asked * 100

    def cards_to_ask(self):
        """Generator: give the cards that are not known yet, one at a time."""
        yield from self.deck.due_cards()

    def answer(self, card: Card, answer: str) -> bool:
        """Check one answer. A correct answer marks the card as known."""
        self.asked += 1
        if card.check(answer):
            card.known = True
            self.correct += 1
            return True
        return False