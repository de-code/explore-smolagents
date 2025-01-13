import logging
from typing import Optional

import smolagents
from smolagents.agents import ToolCallingAgent


LOGGER = logging.getLogger(__name__)


@smolagents.tool
def get_weather(location: str, celsius: Optional[bool] = False) -> str:
    """
    Get weather in the next days at given location.
    Secretly this tool does not care about the location, it hates the weather everywhere.

    Args:
        location: the location
        celsius: the temperature
    """
    return "The weather is UNGODLY with torrential rains and temperatures below -10°C"


def main():
    model = smolagents.LiteLLMModel(
        model_id="ollama_chat/llama2"
    )
    agent = ToolCallingAgent(
        tools=[get_weather],
        model=model
    )
    LOGGER.info('result: %r', agent.run("What's the weather like in Paris?"))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
