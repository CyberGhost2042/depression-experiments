# 🧙‍♂️ AI Terminal RPG – Interactive Text Adventure Game

Welcome to your AI-powered, terminal-based RPG where *you* become the protagonist of a living, breathing narrative — one keystroke at a time.

It’s like Dungeons & Dragons had a baby with ChatGPT, and that baby is now running in your terminal with a memory slightly better than a goldfish (for now 😅).

---

## ✨ What It Does

- Generates **random short story introductions** in fantasy, sci-fi, mystery, and other genres.
- Drops **you** into the story as the lead character with full immersion.
- Lets you control the flow with natural language — your actions shape the story.
- Remembers past inputs in a short-term memory using an in-memory dictionary (`store`) tied to a `session_id`.

---

## 🔍 Tech Stack

- 🧠 LLM: Vertex AI (`gemini-2.0-flash`)
- 🔗 LangChain for chaining prompts and memory handling
- 🧠 Simple in-memory store (`dict`) for now, no persistent database yet
- 🛠️ Terminal-based interaction

---

## 🧪 Current Limitations

Let’s call this a *"Minimum Lovable Prototype"*:

- `session_id` is hardcoded (everyone's playing the same game, awkward...).
- No real user authentication or ID support.
- All story history is wiped after the program exits (RIP your legendary goose chase).
- No vector-based retrieval or deep memory — only recent messages persist.
- No LangSmith tracing wired up yet for debugging chains.

---

## 📦 Setup

```bash
pip install -r requirements.txt
python rpg_game.py