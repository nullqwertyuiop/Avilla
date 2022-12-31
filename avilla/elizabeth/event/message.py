from __future__ import annotations

from typing import TYPE_CHECKING
from avilla.spec.core.message.event import MessageRevoked

from graia.amnesia.message import __message_chain_class__

from avilla.core.context import Context
from avilla.core.message import Message
from avilla.core.selector import Selector
from avilla.core.trait.context import EventParserRecorder
from avilla.spec.core.message import MessageReceived

if TYPE_CHECKING:
    from ..account import ElizabethAccount
    from ..protocol import ElizabethProtocol


event = EventParserRecorder["ElizabethProtocol", "ElizabethAccount"]


@event("GroupMessage")
async def group_message(protocol: ElizabethProtocol, account: ElizabethAccount, raw: dict):
    group = Selector().land(protocol.land.name).group(str(raw["sender"]["group"]["id"]))
    member = group.member(str(raw["sender"]["id"]))
    context = Context(
        account=account,
        client=member,
        endpoint=group,
        scene=group,
        selft=group.member(account.id),
    )
    message_result = await protocol.deserialize_message(context, raw["messageChain"])
    message = Message(
        id=message_result["source"],
        scene=group,
        sender=member,
        content=__message_chain_class__(message_result["content"]),
        time=message_result["time"],
    )
    context._collect_metadatas(message, message)
    event = MessageReceived(context, message)
    return event, context


@event("FriendMessage")
async def friend_message(protocol: ElizabethProtocol, account: ElizabethAccount, raw: dict):
    friend = Selector().land(protocol.land.name).friend(str(raw["sender"]["id"]))
    context = Context(
        account=account,
        client=friend,
        endpoint=friend,
        scene=friend,
        selft=account.to_selector(),
    )
    message_result = await protocol.deserialize_message(context, raw["messageChain"])
    message = Message(
        id=message_result["source"],
        scene=friend,
        sender=friend,
        content=__message_chain_class__(message_result["content"]),
        time=message_result["time"],
    )
    context._collect_metadatas(message, message)
    event = MessageReceived(context, message)
    return event, context


@event("TempMessage")
async def temp_message(protocol: ElizabethProtocol, account: ElizabethAccount, raw: dict):
    group = Selector().land(protocol.land.name).group(str(raw["sender"]["group"]["id"]))
    member = group.member(str(raw["sender"]["id"]))
    context = Context(
        account=account,
        client=member,
        endpoint=member,
        scene=member,
        selft=group.member(account.id),
    )
    message_result = await protocol.deserialize_message(context, raw["messageChain"])
    message = Message(
        id=message_result["source"],
        scene=member,
        sender=member,
        content=__message_chain_class__(message_result["content"]),
        time=message_result["time"],
    )
    context._collect_metadatas(message, message)
    event = MessageReceived(context, message)
    return event, context


@event("GroupRecallEvent")
async def group_recall(protocol: ElizabethProtocol, account: ElizabethAccount, raw: dict):
    group = Selector().land(protocol.land).group(str(raw["group"]["id"]))
    message = group.message(str(raw["message_id"]))
    selft = group.member(account.id)
    if raw["operator"] is None:
        operator = group.member(account.id)
    else:
        operator = group.member(str(raw["operator"]["id"]))
    context = Context(account, operator, message, group, selft)

    return MessageRevoked(context, message, operator), context

@event("FriendRecallEvent")
async def friend_recall(protocol: ElizabethProtocol, account: ElizabethAccount, raw: dict):
    friend = Selector().land(protocol.land).group(str(raw['operator']))
    message = friend.message(str(raw["message_id"]))
    context = Context(account, friend, message, friend, account.to_selector())

    return MessageRevoked(context, message, friend), context