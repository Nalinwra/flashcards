"""Data classes for the flashcards program: Card and Deck."""

from dataclasses import dataclass, field


@dataclass
class Card:
    """One flashcard with a front (question) and a back (answer)."""
    front: str
    back: str
    known: bool = False

    def __post_init__(self) ->None:
        """Clean the text and reject empty cards."""
        self.front = self.front.strip()
        self.back = self.back.strip()
        if not self.front or not self.back:
            raise ValueError("A card needs both a front and a back.")


    def __str__(self) -> str:
        """Show the card as 'front -> back' with a mark if it is known."""
        mark = "[x]" if self.known else "[ ]"
        return f"{mark} {self.front} -> {self.back}"

    def check(self, answer: str) -> bool:
        """Return True if the answer matches the back (ignore case and spaces)."""
        return answer.strip().lower() == self.back.lower()

    def to_dict(self) -> dict:
        """Turn the card into a dict so it can be saved as JSON."""
        return {"front": self.front, "back": self.back, "known": self.known}

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        """Make a card from a dict that was loaded from JSON."""
        return cls(
            front=data["front"],
            back=data["back"],
            known=data.get("known", False),
        )


@dataclass
class Deck:
    """A named group of cards (composition: a Deck has many Cards)."""

    name: str
    cards: list[Card] = field(default_factory=list)

    def __str__(self) -> str:
        """Show the deck name and how many cards are known."""
        return f"{self.name} ({self.known_count}/{len(self.card)} known)"

    @property
    def known_count(self) -> int:
        """Number of cards already marked as known."""
        return sum(1 for card in self.cards if card.known)

    def add_card(self, front: str, back: str) -> Card:
        """Create a card, add it to the deck, and return it."""
        card = Card(front, back)
        self.cards.append(card)
        return card

    def remove_card(self, index: int) -> Card:
        """Remove and return the card at this position (0 is the first)."""
        if not 0 <= index < len(self.cards):
            raise IndexError("No card at that position.")
        return self.cards.pop(index)

    def due_cards(self):
        """Generator: give one card at a time, only cards not known yet."""
        for card in self.cards:
            if not card.known:
                yield card

    def to_dict(self) -> dict:
        """Turn the deck and all its cards into a dict for JSON."""
        return {
            "name": self.name,
            "cards": [card.to_dict() for card in self.cards],
        }    
    @classmethod
    def from_dict(cls, data: dict) -> "Deck":
        """Make a deck from a dict that was loaded from JSON."""
        cards = [Card.from_dict(item) for item in data.get("cards", [])]
        return cls(name=data["name"], cards=cards)