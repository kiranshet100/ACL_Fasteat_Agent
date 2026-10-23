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

def search_recipes(query: str) -> Dict[str, Any]:
    """Search once for recipes and return a compact set of useful results."""
    logging.info("searching for %s", query)
    response = cleint.search(query, max_results=3, search_depth="basic")
    # Search providers can return long snippets and raw metadata. Keep only
    # the fields the model needs to choose and cite a recipe.
    return {
        "results": [
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", "")[:1200],
            }
            for result in response.get("results", [])
        ]
    }


@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for a recipe."""
    return search_recipes(query)
