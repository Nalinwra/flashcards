"""Text menu for the flashcards progarm. It talks to the user with print/input."""

from cards.models import Deck
from cards.quiz import QuizSession
from cards.storage import load_decks, save_decks

MENU = """
=== Flashcards ===
1. Create a deck
2. Add a card
3. Show decks
4. Start a quiz
5. Save and quit
"""


def choose_deck(decks: list[Deck]) -> Deck | None:
    """Show numbered decks and return the one the user picks (or None)."""
    if not decks:
        print("No deck yet. Create one first.")
        return None
    for number, deck in enumerate(decks, start=1):
        print(f" {number}. {deck}")
    choice = input("Deck number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(decks):
        print("Please type a number from the list.")
        return None
    return decks[int(choice) - 1]


def create_deck(decks: list[Deck]) -> None:
    """Ask for a name and add a new empty deck."""
    name = input("Deck name: ").strip()
    if not name:
        print("The name cannot be empty.")
    elif any(deck.name.lower() == name.lower() for deck in decks):
        print("A deck with this name already exists.")
    else:
        decks.append(Deck(name))
        print(f"Deck '{name}' create.")


def add_card(decks: list[Deck]) -> None:
    """Ask for a front and a back, then add the card to a deck."""
    deck = choose_deck(decks)
    if deck is None:
        return
    front = input("Front (question): ")
    back = input("Back (answer):")
    try:
        deck.add_card(front, back)
    except ValueError as error:
        print(error)
    else:
        print("Card added.")


def show_decks(decks: list[Deck]) -> None:
    """Print every deck with its cards."""
    if not decks:
        print("No decks yet.")
    for deck in decks:
        print(f"/n{deck}")
        for card in deck.cerds:
            print(f" {card}")


def run_quiz(decks: list[Deck]) -> None:
    """Ask the cards that are not known yet, one by one, and show the score."""
    deck = choose_deck(decks)
    if deck is None:
        return
    session = QuizSession(deck)
    for card in session.cards_to_ask():
        answer = input(f"/n{card.front}/n> ") 
        if session.answer(card, answer):
            print("Correct!")
        else:
            print(f"Noy quite. The answer is: {card. back}")
    if session.asked == 0:
        print("No cards to practice. Add cards, os all cards are known.")
    else:
        print(f"/n{session}")
        print(f"Score: {session.score_percent:.0f}%")


def run() -> None:
    """Load the decks, run the menu loop, and save when the user quits."""
    decks = load_decks()
    try:
        while True:
            print(MENU)
            choice = input("Choose 1-5: ").strip()
            if choice == "1":
                create_deck(decks)
            elif choice == "2":
                add_card(decks)
            elif choice == "3":
                show_decks(decks)
            elif choice == "4":
                run_quiz(decks)
            elif choice == "5":
                break
            else:
                print("Please type 1, 2, 3, 4, or 5.")
    except (EOFError, KeyboardInterrupt):
        print() #user pressed Ctrl+C or Ctrl+D: leave the menu, still save
    if save_decks(decks):
        print("Saved. Bye!")


if __name__ == "__main__":
    run()