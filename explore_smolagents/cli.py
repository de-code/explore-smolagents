import argparse
import logging
import traceback

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor

import litellm
import smolagents  # type: ignore
from smolagents.agents import (  # type: ignore
    ActionStep,
    CodeAgent,
    ManagedAgent,
    MultiStepAgent,
    ToolCallingAgent
)

from explore_smolagents.weather import get_weather


LOGGER = logging.getLogger(__name__)


def get_model(
    model_id: str,
    model_type: str = 'litellm',
    api_base: str | None = None,
    api_key: str | None = None
) -> smolagents.Model:
    LOGGER.info('model_type: %r', model_type)
    LOGGER.info('model_id: %r', model_id)
    if model_type == 'litellm':
        return smolagents.LiteLLMModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        )
    if model_type == 'openai':
        return smolagents.OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        )
    raise KeyError(f'Unsupported model type: {model_type}')


def do_step_callback(step_log: ActionStep):
    LOGGER.info('step_log: %r', step_log)
    if step_log.error:
        LOGGER.warning('Caught error: %s', '\n'.join(traceback.format_exception(step_log.error)))


def get_agent(
    model: smolagents.Model,
    enable_code_execution: bool
) -> MultiStepAgent:
    agent = ToolCallingAgent(
        tools=[get_weather, smolagents.DuckDuckGoSearchTool],
        model=model,
        step_callbacks=[do_step_callback]
    )
    if not enable_code_execution:
        return agent
    managed_agent = ManagedAgent(
        agent=agent,
        name="managed_agent",
        description="This is an agent that can do web search."
    )
    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[managed_agent],
        step_callbacks=[do_step_callback]
    )
    return manager_agent


def run(
    agent: MultiStepAgent,
    task_prompt: str
):
    LOGGER.info('result: %r', agent.run(task_prompt))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model-type',
        choices=['litellm', 'openai'],
        default='litellm'
    )
    parser.add_argument('--model-id', default='ollama_chat/llama3.2')
    parser.add_argument('--api-base')
    parser.add_argument('--api-key')
    parser.add_argument('--otlp-endpoint')
    parser.add_argument('--task-prompt', default="What's the weather like in Paris?")
    parser.add_argument('--enable-code-execution', action='store_true')
    return parser.parse_args()


def configure_otlp(otlp_endpoint: str):
    LOGGER.info('Configuring OTLP: %r', otlp_endpoint)
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(otlp_endpoint)))
    SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)


def main():
    args = parse_args()
    if args.otlp_endpoint:
        configure_otlp(args.otlp_endpoint)
    run(
        agent=get_agent(
            model=get_model(
                model_type=args.model_type,
                model_id=args.model_id,
                api_base=args.api_base,
                api_key=args.api_key
            ),
            enable_code_execution=args.enable_code_execution
        ),
        task_prompt=args.task_prompt
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
