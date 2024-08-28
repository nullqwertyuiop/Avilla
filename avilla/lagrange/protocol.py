from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from avilla.core.application import Avilla
from avilla.core.protocol import BaseProtocol, ProtocolConfig
from graia.ryanvk import merge, ref

from .instance.client import LagrangeClient
from .service import LagrangeService


@dataclass
class LagrangeConfig(ProtocolConfig):
    uin: int
    protocol: Literal["linux", "macos", "windows"] = "linux"
    sign_url: str | None = None
    device_info_path = "./device.json"
    sign_info_path = "./sig.bin"
    qrcode_path = "./qrcode.png"


def _import_performs():  # noqa: F401
    pass


_import_performs()


class LagrangeProtocol(BaseProtocol):
    service: LagrangeService

    artifacts = {**merge()}

    def __init__(self):
        self.service = LagrangeService(self)

    def ensure(self, avilla: Avilla):
        self.avilla = avilla

        avilla.launch_manager.add_component(self.service)

    def configure(self, config: LagrangeConfig):
        self.service.instances.append(LagrangeClient(self, config))
        return self
