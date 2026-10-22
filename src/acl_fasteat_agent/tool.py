from tavily import TavilyClient
from typing import Dict,Any
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

cleint=TavilyClient()

@tool
def web_search(query:str)-> Dict[str,any]:
    """tool for searching  web for the information"""
    return cleint.search(query)