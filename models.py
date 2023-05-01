from dataclasses import dataclass
from datetime import datetime
from typing import List
import uuid
import xml.etree.ElementTree as ET


class User:
    def __init__(self, user_id: int, name: str, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.personal_chats: List[PersonalChat] = []
        self.group_chats: List[GroupChat] = []

    def __eq__(self, other):
        if isinstance(other, User):
            return self.email == other.email
        else:
            return False

    def to_xml(self) -> ET.Element:
        user_node = ET.Element('user')
        user_node.set('user_id', str(self.user_id))
        name_node = ET.SubElement(user_node, 'name')
        name_node.text = self.name
        email_node = ET.SubElement(user_node, 'email')
        email_node.text = self.email
        password_node = ET.SubElement(user_node, 'password')
        password_node.text = self.password
        group_chats_node = ET.SubElement(user_node, 'group_chats')
        for group_chat in self.group_chats:
            group_chats_node.append(group_chat.to_xml())
        # personal_chats_node = ET.SubElement(user_node, 'personal-chats')
        # for personal_chat in self.personal_chats:
        #     personal_chats_node.append(personal_chat.to_xml())
        return user_node

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )


@dataclass(frozen=True)
class Content:
    text: str
    image_ref: str
    video_ref: str


class Message:
    def __init__(self, message_id: int, sender: User, chat, content: Content):
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
    def __init__(self, group_chat_id: int, name: str, members: List[User]):
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

    def to_xml(self) -> ET.Element:
        group_chat_node = ET.Element('group_chat')
        group_chat_node.set('group_chat_id', str(self.group_chat_id))
        name_node = ET.SubElement(group_chat_node, 'name')
        name_node.text = self.name
        creator_node = ET.SubElement(group_chat_node, 'creator')
        creator_node.text = str(self.creator.user_id)
        members_node = ET.SubElement(group_chat_node, 'members')
        for member in self.members:
            member_node = ET.SubElement(members_node, 'member')
            member_node.set('user_id', str(member.user_id))
        admins_node = ET.SubElement(group_chat_node, 'admins')
        for admin in self.admins:
            admin_node = ET.SubElement(admins_node, 'admin')
            admin_node.text = str(admin.user_id)
        # messages_node = ET.SubElement(group_chat_node, 'messages')
        # for message in self.messages:
        #     messages_node.append(message.to_xml())
        # calls_node = ET.SubElement(group_chat_node, 'calls')
        # for call in self.calls:
        #     calls_node.append(call.to_xml())
        return group_chat_node

    def to_dict(self):
        return {
            "group_chat_id": self.group_chat_id,
            "name": self.name,
            "members": [member.to_dict() for member in self.members]
        }

    @classmethod
    def from_dict(cls, data):
        members = [User.from_dict(member_data) for member_data in data["members"]]
        return cls(
            group_chat_id=data["group_chat_id"],
            name=data["name"],
            members=members
        )


class PersonalChat:
    def __init__(self, personal_chat_id: int, user1: User, user2: User):
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
    def __init__(self, call_id: int, caller: User):
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


def create_group_chat(group_chat_id: int, name: str, members: List[User]) -> GroupChat:
    # group_chat_id = int(uuid.uuid4())
    group_chat = GroupChat(group_chat_id, name, members)
    # for member in members:
    #     if group_chat not in member.group_chats:
    #         member.group_chats.append(group_chat)
    return group_chat


def create_user(user_id: int, name: str, email: str, password: str) -> User:
    # user_id = int(uuid.uuid4())
    user = User(user_id, name, email, password)
    return user


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
    message_id = int(uuid.uuid4())
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
