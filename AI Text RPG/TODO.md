###### TODO LIST

- [ ] Replace hardcoded session_id with proper UUID-based session creation.
- [ ] Add user_id support so each player can continue their own unique adventure.
- [ ] Migrate from InMemoryHistory to a real database (`PostgreSQL maybe....`) .
- [ ] Use `PGVector` to store long-term memory and retrieve relevant story chunks.
- [ ] Add `LangSmith tracing` to observe how chains are behaving under the hood.
- [ ] Split logic into clean modules: `prompt.py, models.py, runners.py` etc.
- [ ] Create save/load functionality for persistent game states.
- [ ] Refactor to support branching story paths and maybe even multiple players (`multiplayer dungeon anyone?`) - trying to implement secure way to share a store chat.
- [ ] Update and modularize the prompt template for dynamic tone, genre, etc.
