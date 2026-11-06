# Cloud Financial

Team Cloud's app for the North American AI Challenge.

Cloud Financial is a wallet app for someone living on their own for the first time on a monthly allowance. Its core feature is **"safe to spend today"**: it tells the user how much they can spend today so their money lasts the whole month. An AI helper explains each purchase in plain language.

---

## Project structure

```
cloud-app/
├── UX-UI.py           # FRONT END: screens and buttons (run this file)
├── safe_to_spend.py   # BACK END: budget math and AI messages
├── notes/             # team notes
└── README.md
```

---

## Requirements

- Python 3.10 or newer
- [Flet](https://flet.dev), the Python UI library the app is built on
- [Anthropic Python SDK](https://pypi.org/project/anthropic/), for the AI helper
- An Anthropic API key in the `ANTHROPIC_API_KEY` environment variable (optional: without it, the AI helper shows "offline" and everything else still works)

---

## Run the app

1. **Get the files:** download these two files from the repository into the same folder:
   ```
   UX-UI.py
   safe_to_spend.py
   ```
   `UX-UI.py` imports `safe_to_spend.py`, so **keep both files in the same folder**.
2. **Install the libraries:**
   ```
   pip install flet anthropic
   ```
3. **Run the app:**
   ```
   python UX-UI.py
   ```

If `python` isn't found, try `python3` or `py`.

---

## AI helper

The AI helper comments on each purchase when **"Ask AI about each purchase"** is checked. Each comment uses API credits, so uncheck the box to save them.


---

## Team

- Kevin + Jose: backend and front end coders
- JJ: pitch script, Cleo / YNAB / Copilot comparison, essays
- Manuel: essays
- Sam: canvas update, slides

## Future enhancements

- Tap-to-purchase, sticker links
- Hardware: order NFC stickers, design/print card, test tap, program stickers
- Physical card with NFC tap for the demo
- Simulated data only, no real payments

Challenge partner notes: see `notes/challenge-partner-notes.md`.
