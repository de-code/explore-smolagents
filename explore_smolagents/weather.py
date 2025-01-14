import logging
from typing import Optional

from smolagents import tool  # type: ignore


LOGGER = logging.getLogger(__name__)


@tool
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
