import logging

import smolagents  # type: ignore
from smolagents.agents import ToolCallingAgent  # type: ignore

from explore_smolagents.weather import get_weather


LOGGER = logging.getLogger(__name__)


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
