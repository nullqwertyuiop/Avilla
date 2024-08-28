from __future__ import annotations

from typing import TYPE_CHECKING, Set

from launart import Launart, Service, any_completed

from .instance.client import LagrangeClient

if TYPE_CHECKING:
    from .protocol import LagrangeProtocol


class LagrangeService(Service):
    id = "lagrange.service"

    protocol: LagrangeProtocol
    instances: list[LagrangeClient]
    account_map: dict[int, LagrangeClient]

    def __init__(self, protocol: LagrangeProtocol):
        self.protocol = protocol
        self.instances = []
        self.account_map = {}
        super().__init__()

    def has_instance(self, account_id: str):
        return int(account_id) in self.account_map

    def get_instance(self, account_id: str) -> LagrangeClient:
        return self.account_map[int(account_id)]

    async def launch(self, manager: Launart):
        async with self.stage("preparing"):
            for i in self.instances:
                manager.add_component(i)

        async with self.stage("blocking"):
            await any_completed(
                manager.status.wait_for_sigexit(), *(i.status.wait_for("blocking-completed") for i in self.instances)
            )

        async with self.stage("cleanup"):
            ...

    @property
    def stages(self):
        return {"preparing", "blocking", "cleanup"}

    @property
    def required(self) -> Set[str]:
        return set()
