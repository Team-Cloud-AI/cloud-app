# AI Use Disclosure

## How the team used AI tools
- **Claude (Anthropic)** helped explain programming concepts, review code, and draft documentation and presentation text.
- Team members wrote the app code and can explain it.
- Competition organizers confirmed AI use is allowed.

## How the app uses AI
- `safe_to_spend.py` (`Wallet.ask_ai`) sends the purchase name and amount, money left for the month and today, savings progress, and under-budget streak to Claude through the Anthropic API.
- A system prompt (`AI_PROMPT`) sets the AI's tone: calm, supportive guidance that helps the user decide rather than blocking purchases.
- The app shows Claude's reply as a personalized message about the purchase.

## Data and keys
- The demo uses simulated data only, with no real payments or bank data.
- No API key is stored in this repository. The app reads it from the `ANTHROPIC_API_KEY` environment variable and shows "AI is offline" without it.
