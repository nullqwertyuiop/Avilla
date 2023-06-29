from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from ..common.collect import BaseCollector
from ..context import processing_isolate, processing_protocol

if TYPE_CHECKING:
    from ...account import BaseAccount
    from ...protocol import BaseProtocol


TProtocol = TypeVar("TProtocol", bound="BaseProtocol")
TAccount = TypeVar("TAccount", bound="BaseAccount")

TProtocol1 = TypeVar("TProtocol1", bound="BaseProtocol")
TAccount1 = TypeVar("TAccount1", bound="BaseAccount")

T = TypeVar("T")
T1 = TypeVar("T1")


class ProtocolBasedPerformTemplate:
    __collector__: ClassVar[BaseCollector]

    protocol: BaseProtocol
    account: BaseAccount


class ProtocolCollector(Generic[TProtocol, TAccount], BaseCollector):
    post_applying: bool = False

    def __init__(self):
        super().__init__()
        self.artifacts["lookup"] = {}

    @property
    def _(self):
        class perform_template(
            super()._,
            Generic[TProtocol1, TAccount1],
            ProtocolBasedPerformTemplate,
            self._base_ring3(),
        ):
            __native__ = True

            protocol: TProtocol1
            account: TAccount1

            def __init__(self, protocol: TProtocol1, account: TAccount1):
                self.protocol = protocol
                self.account = account

        return perform_template[TProtocol, TAccount]

    def __post_collect__(self, cls: type[ProtocolBasedPerformTemplate]):
        super().__post_collect__(cls)
        if self.post_applying:
            if (isolate := processing_isolate.get(None)) is not None:
                isolate.apply(cls)
            if (protocol := processing_protocol.get(None)) is None:
                raise RuntimeError("expected processing protocol")
            protocol.isolate.apply(cls)