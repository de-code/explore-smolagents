import logging
from typing import Optional

import smolagents  # type: ignore
from smolagents.agents import ToolCallingAgent  # type: ignore


LOGGER = logging.getLogger(__name__)


@smolagents.tool
def get_weather(
    location: str,  # pylint: disable=unused-argument
    celsius: Optional[bool] = False  # pylint: disable=unused-argument
) -> str:
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
        model_id="ollama_chat/llama3.2"
    )
    agent = ToolCallingAgent(
        tools=[get_weather],
        model=model
    )
    LOGGER.info('result: %r', agent.run("What's the weather like in Paris?"))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
