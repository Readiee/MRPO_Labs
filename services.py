import uuid
from typing import List

from models import GroupChat, User, Content, Message
from repositories import AbstractRepository


def create_user(name: str, email: str, password: str) -> User:
    user_id = str(uuid.uuid4())
    user = User(user_id, name, email, password)
    return user


def create_group_chat(name: str, members: List[User]) -> GroupChat:
    group_chat_id = str(uuid.uuid4())
    group_chat = GroupChat(group_chat_id, name, members)
    for member in members:
        member.group_chats.append(group_chat)
    return group_chat


def add_user_to_group_chat(member: User, group_chat: GroupChat):
    group_chat.add_member(member)
    if group_chat not in member.group_chats:
        member.group_chats.append(group_chat)


def remove_user_from_group_chat(member: User, group_chat: GroupChat):
    group_chat.remove_member(member)
    if group_chat in member.group_chats:
        member.group_chats.remove(group_chat)


def make_admin_of_group_chat(user: User, group_chat: GroupChat):
    group_chat.make_admin(user)


def send_message(sender: User, chat: GroupChat, content: Content):
    message_id = str(uuid.uuid4())
    message = Message(message_id, sender, chat, content)
    chat.messages.append(message)


def delete_message(message: Message, chat: GroupChat):
    if message in chat.messages:
        chat.messages.remove(message)


def find_messages_by_text(text: str, chat: GroupChat) -> List[Message]:
    founded_results = []
    for message in chat.messages:
        if text in message.content.text:
            founded_results.append(message)
    return founded_results
