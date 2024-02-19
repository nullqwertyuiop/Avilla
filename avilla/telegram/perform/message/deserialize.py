from __future__ import annotations

from typing import TYPE_CHECKING

from avilla.core.ryanvk.collector.application import ApplicationCollector
from graia.ryanvk import OptionalAccess

if TYPE_CHECKING:
    from avilla.core.context import Context
    from avilla.telegram.account import TelegramAccount


class TelegramMessageDeserializePerform((m := ApplicationCollector())._):
    m.namespace = "avilla.protocol/telegram::message"
    m.identify = "deserialize"

    context: OptionalAccess[Context] = OptionalAccess()
    account: OptionalAccess[TelegramAccount] = OptionalAccess()

    # LINK: https://github.com/microsoft/pyright/issues/5409
