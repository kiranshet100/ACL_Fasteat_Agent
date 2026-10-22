from dotenv import load_dotenv 
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,AIMessage
from prompt import SYSTEM_PROMPT,CHEF_PROMPT
from tool import web_search
from photo_decoder import choose_image_file,build_image_message
import logging
from groq import RateLimitError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
load_dotenv()

logging.info("creating Agent....")
model=init_chat_model(model="qwen/qwen3.8-27b",model_provider="groq",max_retries=0)

agent = create_agent(model=model,tools=[web_search],system_prompt=SYSTEM_PROMPT)
logging.info("chossingg out imaage ....")
path= choose_image_file()
message=build_image_message(path, CHEF_PROMPT)

logging.info("invoking our ageent")
try:
    response = agent.invoke({"messages": [message]})
    print(response["messages"][-1].content)

except RateLimitError as e:
    print("Groq rate limit error:", e)
    print("Response details:", e.response.text)
    print("Retry after:", e.response.headers.get("retry-after"))