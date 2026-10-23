from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from prompt import CHEF_PROMPT, SYSTEM_PROMPT
from tool import search_recipes
from photo_decoder import choose_image_file, build_image_message
import logging
import re
import time
from groq import RateLimitError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
load_dotenv()

logging.info("creating model")
model = init_chat_model(
    model="qwen/qwen3.8-27b",
    model_provider="groq",
    max_retries=0,
    max_tokens=800,
)


def invoke_with_rate_limit_retry(messages, attempts=4):
    """Retry only the failed model call, observing Groq's retry timing."""
    for attempt in range(attempts):
        try:
            return model.invoke(messages)
        except RateLimitError as error:
            if attempt == attempts - 1:
                raise
            retry_after = error.response.headers.get("retry-after")
            body_delay = re.search(
                r"try again in ([0-9.]+)s", error.response.text, re.IGNORECASE
            )
            delay = max(
                1,
                int(float(retry_after)) if retry_after else 0,
                int(float(body_delay.group(1)) + 1) if body_delay else 0,
            )
            logging.warning("Groq rate limit reached; retrying in %s seconds", delay)
            time.sleep(delay)


def main():
    logging.info("choosing image")
    image_path = choose_image_file()
    image_message = build_image_message(image_path, CHEF_PROMPT)
    logging.info("identifying ingredients")
    ingredient_response = invoke_with_rate_limit_retry(
        [SystemMessage(content=CHEF_PROMPT), image_message]
    )
    ingredients = ingredient_response.content

    logging.info("searching once for a recipe")
    results = search_recipes(f"recipe using {ingredients}")

    logging.info("writing recipe")
    final_response = invoke_with_rate_limit_retry(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"Visible ingredients identified: {ingredients}\n\n"
                    f"Recipe search results (choose from these; do not search again):\n{results}"
                )
            ),
        ]
    )
    print(final_response.content)


if __name__ == "__main__":
    main()
