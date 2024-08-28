from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from avilla.core.account import AccountStatus, BaseAccount
from avilla.core.selector import Selector
from avilla.lagrange.instance.client import LagrangeClient

if TYPE_CHECKING:
    from avilla.lagrange.protocol import LagrangeProtocol


@dataclass
class LagrangeAccount(BaseAccount):
    protocol: LagrangeProtocol
    status: AccountStatus

    def __init__(self, route: Selector, protocol: LagrangeProtocol):
        super().__init__(route, protocol.avilla)
        self.protocol = protocol
        self.status = AccountStatus()

    @property
    def connection(self) -> LagrangeClient:
        return self.protocol.service.get_instance(self.route["account"])

    @property
    def available(self) -> bool:
        return self.connection.alive
