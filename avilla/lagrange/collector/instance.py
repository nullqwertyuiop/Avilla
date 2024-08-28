from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from avilla.core.ryanvk.collector.base import AvillaBaseCollector
from graia.ryanvk import Access, BasePerform

if TYPE_CHECKING:
    from avilla.lagrange.instance.client import LagrangeClient
    from avilla.lagrange.protocol import LagrangeProtocol


class InstanceBasedPerformTemplate(BasePerform, native=True):
    __collector__: ClassVar[InstanceCollector]

    protocol: Access[LagrangeProtocol] = Access()
    instance: Access[LagrangeClient] = Access()


class InstanceCollector(AvillaBaseCollector):
    post_applying: bool = False

    @property
    def _(self):
        upper = super()._

        class PerformTemplate(
            InstanceBasedPerformTemplate,
            upper,
            native=True,
        ): ...

        return PerformTemplate
