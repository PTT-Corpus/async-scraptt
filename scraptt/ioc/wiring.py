from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide as _Provide

if TYPE_CHECKING:
    from dependency_injector.providers import Provider
    from dependency_injector.wiring import Modifier


class Provide(_Provide):
    def __init__(
        self, provider: Provider | type, modifier: Modifier | None = None
    ) -> None:
        super().__init__(provider=provider.__qualname__, modifier=modifier)
