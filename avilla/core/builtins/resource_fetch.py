from __future__ import annotations

from ..resource import LocalFileResource, RawResource
from ..ryanvk import Collector


class CoreResourceFetchPerform((m := Collector())._):
    @m.fetch(LocalFileResource)
    async def fetch_localfile(self, res: LocalFileResource):
        return res.file.read_bytes()

    @m.fetch(RawResource)
    async def fetch_raw(self, res: RawResource):
        return res.data
