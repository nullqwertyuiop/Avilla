from __future__ import annotations

from io import BytesIO

from avilla.core import CoreCapability
from avilla.core.ryanvk.collector.protocol import ProtocolCollector
from avilla.telegram.resource import TelegramResource


class TelegramResourceFetchPerform((m := ProtocolCollector["TelegramProtocol"]())._):
    m.namespace = "avilla.protocol/telegram::resource_fetch"

    @m.entity(CoreCapability.fetch, resource=TelegramResource)
    async def fetch_resource(self, resource: TelegramResource) -> bytes:
        b_io = BytesIO()
        await resource.file.download_to_memory(b_io)
        return b_io.getvalue()