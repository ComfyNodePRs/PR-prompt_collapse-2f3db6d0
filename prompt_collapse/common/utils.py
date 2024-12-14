import re
from typing import Any, List

from prompt_collapse.state import State


def find_parameters(value: str) -> List[str]:
    """
    Find all parameters in a string.
    Parameters are defined as words surrounded by curly braces.
    Essentially string placeholders.
    :param value: A string to search for parameters.
    :return: A list of parameters found in the string.
    """
    return [match[1:-1] for match in re.findall(r"{\w+}", value)]


def apply_parameters(value: Any, parameters: List[str], local_state: State) -> Any:
    """
    Apply parameters to a value.
    If the value is not a string, it is returned as is.

    Parameters are replaced in the value using the local state.
    :param value: A value to apply parameters to.
    :param parameters: A list of parameters to apply.
    :param local_state: The local state to use for parameter values.
    :return: The value with parameters applied.
    """
    if not isinstance(value, str):
        return value

    variables = {parameter: local_state.get(parameter) for parameter in parameters}

    return value.format(**variables)
