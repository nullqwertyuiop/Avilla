from __future__ import annotations

from dataclasses import dataclass

from yarl import URL

from avilla.core.application import Avilla
from avilla.core.protocol import BaseProtocol, ProtocolConfig
from avilla.telegram.connection import TelegramLongPollingNetworking
from avilla.telegram.service import TelegramService
from graia.ryanvk import merge, ref


@dataclass
class TelegramLongPollingConfig(ProtocolConfig):
    token: str
    base_url: URL = URL("https://api.telegram.org/")
    timeout: int = 15
    reformat: bool = False


@dataclass
class TelegramWebhookConfig(ProtocolConfig):
    token: str
    webhook_url: URL
    base_url: URL = URL("https://api.telegram.org/")
    reformat: bool = False


def _import_performs():
    # TODO: this is fine

    # isort: off

    # :: Message
    # from .perform.message.deserialize import TelegramMessageDeserializePerform  # noqa: F401
    # from .perform.message.serialize import TelegramMessageSerializePerform  # noqa: F401

    # :: Event
    # from .perform.event.message import TelegramEventMessagePerform  # noqa: F401

    # :: Action
    # from .perform.action.forum import TelegramForumActionPerform  # noqa: F401
    from .perform.action.preference import TelegramPreferenceActionPerform  # noqa: F401

    # from .perform.action.message import TelegramMessageActionPerform  # noqa: F401

    # :: Resource Fetch
    # from .perform.resource_fetch import TelegramResourceFetchPerform  # noqa: F401


class TelegramProtocol(BaseProtocol):
    service: TelegramService

    _import_performs()
    artifacts = {
        **merge(
            # ref("avilla.protocol/telegram::resource_fetch"),
            # ref("avilla.protocol/telegram::action", "forum"),
            ref("avilla.protocol/telegram::action", "preference"),
            # ref("avilla.protocol/telegram::action", "message"),
            # ref("avilla.protocol/telegram::message", "deserialize"),
            # ref("avilla.protocol/telegram::message", "serialize"),
            # ref("avilla.protocol/telegram::event", "message"),
        ),
    }

    def __init__(self):
        self.service = TelegramService(self)

    def ensure(self, avilla: Avilla):
        self.avilla = avilla

        avilla.launch_manager.add_component(self.service)

    def configure(self, config: TelegramLongPollingConfig | TelegramWebhookConfig):
        if isinstance(config, TelegramLongPollingConfig):
            bot = TelegramLongPollingNetworking(self, config)
        elif isinstance(config, TelegramWebhookConfig):
            # TODO: implement webhook
            bot = ...
        else:
            raise ValueError("Invalid config type")
        self.service.instance_map[bot.account_id] = bot
        return self
