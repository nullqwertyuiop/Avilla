from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from lagrange import Client, InfoManager, app_list, sign_provider
from lagrange.client.events import BaseEvent
from launart import Service, any_completed
from launart.manager import Launart
from loguru import logger

from avilla.core.ryanvk.staff import Staff
from avilla.lagrange.capability import LagrangeCapability
from avilla.lagrange.logger import install_loguru
from avilla.twilight.util import gen_subclass

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

    def get_staff_components(self):
        return {"connection": self, "protocol": self.protocol, "avilla": self.protocol.avilla}

    def get_staff_artifacts(self):
        return [self.protocol.artifacts, self.protocol.avilla.global_artifacts]

    @property
    def staff(self):
        return Staff(self.get_staff_artifacts(), self.get_staff_components())

    @property
    def alive(self):
        return self.instance is not None and not self.instance.online.is_set()

    def register_handler(self):
        async def handle(_: Client, event: BaseEvent):
            with suppress(NotImplementedError):
                await LagrangeCapability(self.staff).handle_event(event)

        for sub_event in gen_subclass(BaseEvent):
            self.instance.events.subscribe(sub_event, handle)

    async def login(self):
        if self.info_manager.sig_info.d2:
            if await self.instance.register():
                return True
        return await self.instance.login(qrcode_path=self.config.qrcode_path)

    async def launch(self, manager: Launart):
        install_loguru()
        async with self.stage("preparing"):
            self.info_manager = InfoManager(self.config.uin, self.config.device_info_path, self.config.sign_info_path)
            with self.info_manager:
                self.instance = Client(
                    self.config.uin,
                    app_list[self.config.protocol],
                    self.info_manager.device,
                    self.info_manager.sig_info,
                    sign_provider(sign_url) if (sign_url := self.config.sign_url) else None,
                )
            self.register_handler()

        async with self.stage("blocking"):
            self.instance.connect()
            if not await self.login():
                logger.error(f"Login failed for {self.id}")
                return
            self.info_manager.save_all()
            await any_completed(manager.status.wait_for_sigexit(), self.instance.wait_closed())

        async with self.stage("cleanup"):
            await self.instance.stop()
            self.instance = None
