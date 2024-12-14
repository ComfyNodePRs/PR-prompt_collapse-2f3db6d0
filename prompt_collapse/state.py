from typing import Any


class State:
    def __init__(self) -> None:
        self._variables: dict[str, Any] = {}

    def exists(self, variable: str) -> bool:
        return variable in self._variables

    def get(self, variable: str) -> Any:
        return self._variables.get(variable)

    def set(self, variable: str, value: Any) -> None:
        if variable in self._variables:
            if self._variables[variable] != value:
                raise ValueError(
                    f"Variable {variable} already exists with a different value"
                )

        self._variables[variable] = value

    def update(self, variable: str, value: Any) -> None:
        if variable not in self._variables:
            raise ValueError(f"Variable {variable} does not exist")

        self._variables[variable] = value
