"""Save decks to a JSON file and load  them back on the next run."""

import json
from pathlib import Path

from cards.models import Deck

# The data folder sits next to the cards package, whatever folder you run from.
DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "decks.json"


def save_decks(decks: list[Deck], path: Path = DEFAULT_PATH) -> bool:
    """Save all decks to a JSON File. Return True if it worked."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [deck.to_dict() for deck in decks]
        text = json.dumps(data, indent=2, ensure_ascii=False)
        path.write_text(text, encoding="utf-8")
    except OSError as error:
        print(f"Sorry, the decks could not be saved: {error}")
        return False
    return True


def load_decks(path: Path = DEFAULT_PATH) -> list[Deck]:
    """Load decks from a JSON flie.Return an emoty list if there is a pron=blem."""
    if not path.exists():
        return [] #first run:no file yet,this is normal
    try:
        raw = json.loads(path.read_text(encoding="utf-8")) 
        return [Deck.from_dict(item) for item in raw]
    except (OSError, json.JSONDecodeError) as error:
        print(f"Sorry, the save file could not be read: {error}")
    except (KeyError, TypeError, ValueError) as error:
        print(f"Sorry, the save file has the wrong format: {error!r}")
    return []