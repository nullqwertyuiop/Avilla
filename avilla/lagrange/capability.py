from __future__ import annotations

from typing import TYPE_CHECKING, Any

from graia.amnesia.message import Element, MessageChain

from avilla.core.event import AvillaEvent
from avilla.core.ryanvk.collector.application import ApplicationCollector
from graia.ryanvk import Fn, PredicateOverload, TypeOverload

if TYPE_CHECKING:
    pass


class LagrangeCapability((m := ApplicationCollector())._):
    @Fn.complex({PredicateOverload(lambda _, raw: raw["type"]): ["raw_event"]})
    async def event_callback(self, raw_event: dict) -> AvillaEvent | None: ...

    @Fn.complex({PredicateOverload(lambda _, raw: raw["type"]): ["raw_element"]})
    async def deserialize_element(self, raw_element: dict) -> Element:  # type: ignore
        ...

    @Fn.complex({TypeOverload(): ["element"]})
    async def serialize_element(self, element: Any) -> dict:  # type: ignore
        ...

    async def deserialize_chain(self, chain: list[dict]):
        elements = []

        for raw_element in chain:
            elements.append(await self.deserialize_element(raw_element))

        return MessageChain(elements)

    async def serialize_chain(self, chain: MessageChain):
        elements = []

        for element in chain:
            elements.append(await self.serialize_element(element))

        return elements

    async def handle_event(self, event: dict):
        # TODO: dispatch & handle event
        pass
