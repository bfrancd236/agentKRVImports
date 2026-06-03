import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage

from prompt import SYSTEM_PROMPT
from memory import get_history, add_message

load_dotenv()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.7,
    max_tokens=1024,
)


def run_agent(phone: str, user_message: str) -> str:
    add_message(phone, "human", user_message)
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + get_history(phone)
    response = llm.invoke(messages)
    reply = response.content
    add_message(phone, "ai", reply)
    return reply
