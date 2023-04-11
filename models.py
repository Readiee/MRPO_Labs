from dataclasses import dataclass
from datetime import datetime
from typing import List


class User:
    def __init__(self, user_id: str, name: str, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.personal_chats: List[PersonalChat] = []
        self.group_chats: List[GroupChat] = []

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_id == other.user_id
        else:
            return False


@dataclass(frozen=True)
class Content:
    text: str
    image_ref: str
    video_ref: str


class Message:
    def __init__(self, message_id: str, sender: User, chat, content: Content):
        self.message_id = message_id
        self.sender = sender
        self.chat = chat
        self.content = content
        self.timestamp = datetime.utcnow()

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.message_id == other.message_id
        else:
            return False


class GroupChat:
    def __init__(self, group_chat_id: str, name: str, members: List[User]):
        self.group_chat_id = group_chat_id
        self.name = name
        self.members = members
        self.creator = members[0]
        self.admins: List[User] = []
        self.messages: List[Message] = []
        self.calls: List[Call] = []

    def __eq__(self, other):
        if isinstance(other, GroupChat):
            return self.group_chat_id == other.group_chat_id
        else:
            return False

    def add_member(self, member: User):
        if member not in self.members:
            self.members.append(member)
            member.group_chats.append(self)

    def remove_member(self, member: User):
        if member in self.members:
            self.members.remove(member)
            member.group_chats.remove(self)

    def make_admin(self, member: User):
        if (member in self.members) and (member != self.creator) and (member not in self.admins):
            self.admins.append(member)

    def demote_admin(self, admin: User):
        if admin in self.admins:
            self.admins.remove(admin)


class PersonalChat:
    def __init__(self, personal_chat_id: str, user1: User, user2: User):
        self.personal_chat_id = personal_chat_id
        self.user1 = user1
        self.user2 = user2
        self.messages: List[Message] = []

    def __eq__(self, other):
        if isinstance(other, PersonalChat):
            return self.personal_chat_id == other.personal_chat_id
        else:
            return False


class Call:
    def __init__(self, call_id: str, caller: User):
        self.call_id = call_id
        self.caller = caller
        self.participants: List[User] = [caller]
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.duration = None

    def __eq__(self, other):
        if isinstance(other, Call):
            return self.call_id == other.call_id
        else:
            return False

    def end_call(self):
        self.participants = []
        self.end_time = datetime.utcnow()
        self.duration = self.end_time - self.start_time
