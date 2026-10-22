from tavily import TavilyClient
from typing import Dict,Any
from langchain.tools import tool
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
load_dotenv()

cleint=TavilyClient()

@tool
def web_search(query:str)-> Dict[str,any]:
    """tool for searching  web for the information"""
    logging.info(f"seaaarching for {query}")
    return cleint.search(query)