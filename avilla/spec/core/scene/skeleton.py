from __future__ import annotations

from avilla.core.abstract.trait import Fn, Trait
from avilla.core.utilles.selector import Selector


class SceneTrait(Trait):
    @Fn.bound_entity
    async def leave(self) -> None:
        ...

    @Fn.bound_entity
    async def disband(self) -> None:
        ...

    @Fn.bound_entity
    async def remove_member(self, reason: str | None = None) -> None:
        ...

    # TODO: join, invite etc.
