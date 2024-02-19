from __future__ import annotations

from datetime import datetime

from avilla.core.context import Context
from avilla.core.message import Message
from avilla.core.selector import Selector
from avilla.standard.core.message import MessageReceived
from avilla.telegram.capability import TelegramCapability
from avilla.telegram.collector.connection import ConnectionCollector


class TelegramEventMessagePerform((m := ConnectionCollector())._):
    m.namespace = "avilla.protocol/telegram::event"
    m.identify = "message"

    @m.entity(TelegramCapability.event_callback, event_type="message.private")
    @m.entity(TelegramCapability.event_callback, event_type="message.group")
    @m.entity(TelegramCapability.event_callback, event_type="message.supergroup")
    async def message_private(self, event_type: str, raw_event: dict):
        self_id = self.connection.account_id
        account = self.account
        chat = Selector().land(account.route["land"]).chat(str(raw_event["message"]["chat"]["id"]))
        if event_type == "message.supergroup" and raw_event["message"]["message_thread_id"]:
            chat = chat.thread(str(raw_event["message"]["message_thread_id"]))
        context = Context(
            account,
            chat.member(raw_event["message"]["from"]["id"]),
            chat,
            chat,
            Selector().land(account.route["land"]).account(self_id)
            if event_type == "message.private"
            else chat.member(str(self_id)),
        )

        # TODO: re-implement MediaGroup

        # if media_group_id := raw_event.message.media_group_id:
        #     cache: Memcache = self.instance.protocol.avilla.launch_manager.get_component(MemcacheService).cache
        #     cached = await cache.get(f"telegram/update(media_group):{media_group_id}")
        #     decomposed = MessageFragment.sort(*cached)
        # else:
        #     decomposed = MessageFragment.decompose(raw_event.message, raw_event)

        # TODO: re-implement decompose

        decomposed: list[dict] = ...

        message = await TelegramCapability(account.staff.ext({"context": context})).deserialize(decomposed)
        reply = raw_event["message"]["reply_to_message"]

        return MessageReceived(
            context,
            Message(
                id=str(raw_event["message"]["message_id"]),
                scene=chat,
                sender=chat.member(raw_event["message"]["from"]["id"]),
                content=message,
                time=datetime.fromtimestamp(raw_event["message"]["date"]),
                reply=reply,
            ),
        )
