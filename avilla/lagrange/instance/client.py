from __future__ import annotations

from typing import TYPE_CHECKING

from lagrange import Client, InfoManager, app_list, sign_provider
from launart import Service
from launart.manager import Launart
from loguru import logger

if TYPE_CHECKING:
    from avilla.lagrange.protocol import LagrangeConfig, LagrangeProtocol


class LagrangeClient(Service):
    required: set[str] = set()
    stages: set[str] = {"preparing", "blocking", "cleanup"}

    protocol: LagrangeProtocol
    config: LagrangeConfig

    instance: Client | None = None
    info_manager: InfoManager | None = None

    def __init__(self, protocol: LagrangeProtocol, config: LagrangeConfig) -> None:
        super().__init__()
        self.protocol = protocol
        self.config = config
        self.account_id = self.config.uin

    @property
    def id(self):
        return f"lagrange/client#{self.account_id}"

    async def wait_for_available(self):
        await self.status.wait_for_available()

    @property
    def alive(self):
        return self.instance is not None and not self.instance.online.is_set()

    async def login(self):
        if self.info_manager.sig_info.d2:
            if not await self.instance.register():
                return await self.instance.login()
            return True
        return await self.instance.login()

    async def launch(self, manager: Launart):
        async with self.stage("preparing"):
            self.info_manager = InfoManager(self.config.uin, self.config.device_info_path, self.config.sign_info_path)

        async with self.stage("blocking"):
            with self.info_manager as info_manager:
                self.instance = Client(
                    self.config.uin,
                    app_list[self.config.protocol],
                    info_manager.device,
                    info_manager.sig_info,
                    sign_provider(sign_url) if (sign_url := self.config.sign_url) else None,
                )
                self.instance.connect()
                if not await self.login():
                    logger.error(f"Login failed for {self.id}")
                    return

        async with self.stage("cleanup"):
            await self.instance.stop()
            self.instance = None
