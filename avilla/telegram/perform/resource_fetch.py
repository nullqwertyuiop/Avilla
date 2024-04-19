from __future__ import annotations

from typing import TYPE_CHECKING

from avilla.core import Context, CoreCapability, Selector
from avilla.core.ryanvk.collector.account import AccountCollector
from avilla.telegram.resource import (
    TelegramAnimationResource,
    TelegramAudioResource,
    TelegramDocumentResource,
    TelegramFileResource,
    TelegramPhotoResource,
    TelegramResource,
    TelegramStickerResource,
    TelegramVideoNoteResource,
    TelegramVideoResource,
    TelegramVoiceResource,
)
from graia.ryanvk import OptionalAccess

if TYPE_CHECKING:
    from avilla.telegram.account import TelegramAccount  # noqa
    from avilla.telegram.protocol import TelegramProtocol  # noqa


class TelegramResourceFetchPerform((m := AccountCollector["TelegramProtocol", "TelegramAccount"]())._):
    m.namespace = "avilla.protocol/telegram::resource_fetch"

    context: OptionalAccess[Context] = OptionalAccess()

    @m.entity(CoreCapability.fetch, resource=TelegramResource)
    @m.entity(CoreCapability.fetch, resource=TelegramPhotoResource)
    @m.entity(CoreCapability.fetch, resource=TelegramAnimationResource)
    @m.entity(CoreCapability.fetch, resource=TelegramAudioResource)
    @m.entity(CoreCapability.fetch, resource=TelegramDocumentResource)
    @m.entity(CoreCapability.fetch, resource=TelegramVideoResource)
    @m.entity(CoreCapability.fetch, resource=TelegramVideoNoteResource)
    @m.entity(CoreCapability.fetch, resource=TelegramVoiceResource)
    @m.entity(CoreCapability.fetch, resource=TelegramStickerResource)
    async def fetch_resource(self, resource: TelegramResource) -> bytes:
        resp = await self.account.connection.call("getFile", file_id=resource.file_id)
        file: dict = resp["result"]
        file_id = file["file_id"]
        file_unique_id = file["file_unique_id"]
        file_selector = Selector().land(self.context.land).file_id(file_id).file_unique_id(file_unique_id)
        file_resource = TelegramFileResource(
            selector=file_selector,
            file_id=file_id,
            file_unique_id=file_unique_id,
            file_size=file.get("file_size"),
            file_path=file.get("file_path"),
        )
        return await self.fetch_file_resource(file_resource)

    @m.entity(CoreCapability.fetch, resource=TelegramFileResource)
    async def fetch_file_resource(self, resource: TelegramFileResource) -> bytes:
        connection = self.account.connection
        url = connection.config.file_base_url / f"bot{connection.config.token}" / resource.file_path
        async with connection.session.get(url, proxy=connection.config.proxy) as resp:
            return await resp.read()
