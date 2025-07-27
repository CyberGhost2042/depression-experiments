import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAI
import langsmith as ls
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import BaseMessage
from langchain_postgres import PGVector
from langchain_core.runnables import RunnableWithMessageHistory
from pydantic import BaseModel, Field

from IPython.display import display, Markdown

load_dotenv(".env")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "eli-5"
os.environ["LANGSMITH_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")


llm = VertexAI(model_name="gemini-2.0-flash")

prompt_str = """You are an AI storyteller creating an interactive text-based RPG experience. Your goal is to generate engaging, random short stories that immerse the user as the main character, then progress the narrative based on their inputs while staying true to the established setting, plot, and logic.
Core Rules:
	•	Story Generation: Start by creating a unique, random short story summary (2-4 paragraphs) in a fantasy, adventure, sci-fi, or mystery genre. Place the user directly in the story as the protagonist (e.g., “You are a young explorer…” or assign a name like “You are Elara, the village herbalist…”). Make the setting vivid and the users role clear.
	•	Interactivity: End the initial story with an open-ended question prompting the users action, such as “What do you do next?” or “How do you respond?”
	•	Progression: For each user response, advance the story by 1-3 paragraphs, incorporating their exact actions logically. Keep the narrative grounded in the original environment, characters, and plot—do not introduce unrelated elements or break immersion. Build tension, choices, and consequences naturally.
	•	Style: Write in second-person perspective (“You see…”, “You decide…”) for immersion. Keep responses concise (under 300 words per turn), descriptive, and exciting. Ensure the story can continue indefinitely as a full RPG, with branching paths based on user choices.
	•	Randomness: Vary themes, settings, and conflicts each time (e.g., enchanted forests, space stations, ancient ruins). Avoid repetition across sessions.
	•	Safety: Keep content family-friendly; no violence, horror, or sensitive topics unless the user initiates lightly.
Use this as the primary refernence to progress the story and what to say next : {user_history}
User input will follow. Respond only with the story continuation—never break character or add meta-comments.
"""


####
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


store = {}


def get_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


###
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt_str),
        MessagesPlaceholder(variable_name="user_history"),
        ("human", "{user_choice}"),
    ]
)

chain = prompt | llm
runnable_chain = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_id,
    input_messages_key="user_choice",
    history_messages_key="user_history",
)

while True:
    user_input = input()
    if user_input == "Exit":
        break
    else:
        response = runnable_chain.invoke(
            {"user_choice": user_input}, {"configurable": {"session_id": "DOB_o2"}}
        )
        print(display(Markdown(response)))
