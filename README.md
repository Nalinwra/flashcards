# Flashcards

A flashcard program that lets users make decks of cards, practice them in a
quiz, and save their progress in a file.

Final project for CS105BKK. Works alone, no extra packages needed to run.

## What it does

- Create decks and add cards (a front and a back).
- Take a quiz. Cards you answer correctly are marked as known and are skipped
  next time.
- Everything is saved to `data/decks.json` and loaded again on the next run.
- Bad input (wrong menu choice, empty card, missing or broken file) shows a
  short message instead of crashing.

## Requirements

- Python 3.12 or newer

Check your version:

- Windows: `python --version`
- macOS: `python3 --version`

## How to run

Open a terminal in the project folder (the one that contains `main.py`).

**Windows**

```
python main.py
```

**macOS**

```
python3 main.py
```

You will see a menu. Type a number (1 to 5) and press Enter.

## How to run the tests and the style check

Install the two tools once:

- Windows: `python -m pip install pytest ruff`
- macOS: `python3 -m pip install pytest ruff`

Then:

```
python -m pytest
python -m ruff check .
```

On macOS use `python3` instead of `python`.

## Project structure

```
flashcards/
├── main.py            # starts the program
├── cards/
│   ├── __init__.py
│   ├── models.py      # Card and Deck classes
│   ├── quiz.py        # QuizSession class (checks answers, keeps the score)
│   ├── storage.py     # saves and loads JSON with pathlib
│   └── cli.py         # the text menu
└── tests/
    └── test_flashcards.py
```

## Design choice

`QuizSession` only checks answers and counts the score. It never prints or
asks for input. All printing and typing is in `cli.py`. This keeps each part
simple and makes the quiz easy to test.