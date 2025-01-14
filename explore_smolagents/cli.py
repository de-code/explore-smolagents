import argparse
import logging

import litellm
import smolagents  # type: ignore
from smolagents.agents import ToolCallingAgent  # type: ignore

from explore_smolagents.weather import get_weather


LOGGER = logging.getLogger(__name__)


def run(
    model_id: str,
    api_base: str | None = None,
    api_key: str | None = None
):
    LOGGER.info('model_id: %r', model_id)
    model = smolagents.LiteLLMModel(
        model_id=model_id,
        api_base=api_base,
        api_key=api_key
    )
    agent = ToolCallingAgent(
        tools=[get_weather],
        model=model
    )
    LOGGER.info('result: %r', agent.run("What's the weather like in Paris?"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-id', default='ollama_chat/llama3.2')
    parser.add_argument('--api-base')
    parser.add_argument('--api-key')
    return parser.parse_args()


def main():
    args = parse_args()
    litellm.set_verbose = True
    run(
        model_id=args.model_id,
        api_base=args.api_base,
        api_key=args.api_key
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
