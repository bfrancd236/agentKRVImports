from collections import defaultdict
from langchain_core.messages import HumanMessage, AIMessage

conversation_history: defaultdict[str, list] = defaultdict(list)


def get_history(phone: str) -> list:
    return conversation_history[phone]


def add_message(phone: str, role: str, content: str) -> None:
    if role == "human":
        conversation_history[phone].append(HumanMessage(content=content))
    else:
        conversation_history[phone].append(AIMessage(content=content))


def clear_history(phone: str) -> None:
    conversation_history[phone] = []
