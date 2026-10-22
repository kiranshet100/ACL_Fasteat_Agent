from dotenv import load_dotenv 
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,AIMessage
from prompt import SYSTEM_PROMPT,CHEF_PROMPT

load_dotenv()

model=init_chat_model(model="openai/gpt-oss-20b",model_provider="groq")

agent = create_agent(model=model,system_prompt=SYSTEM_PROMPT)
#query = input("Enter your question about the image: ").strip()
response = agent.invoke({"messages":[HumanMessage(content="hello how are ")]})

print(response["messages"][-1].content)