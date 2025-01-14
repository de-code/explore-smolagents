import argparse
import logging

import smolagents  # type: ignore
from smolagents.agents import ToolCallingAgent  # type: ignore

from explore_smolagents.weather import get_weather


LOGGER = logging.getLogger(__name__)


def run(model_id: str):
    LOGGER.info('model_id: %r', model_id)
    model = smolagents.LiteLLMModel(
        model_id=model_id
    )
    agent = ToolCallingAgent(
        tools=[get_weather],
        model=model
    )
    LOGGER.info('result: %r', agent.run("What's the weather like in Paris?"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-id', default='ollama_chat/llama3.2')
    return parser.parse_args()


def main():
    args = parse_args()
    run(model_id=args.model_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
