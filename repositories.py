import json
import os
from abc import ABC, abstractmethod
from typing import Optional
from xml.etree.ElementTree import Element

import models
from models import *


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, obj_id: int):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def delete(self, obj_id: int):
        pass


# JSON Repositories

class UserJSONRepository(AbstractRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_by_id(self, user_id: int) -> Optional[User]:
        users = self.get_all()
        for user in users:
            if user.user_id == user_id:
                return user
        return None

    def get_all(self) -> List[User]:
        if os.stat(self.file_path).st_size == 0:
            return []
        with open(self.file_path, "r") as file:
            data = json.loads(file.read())
            users_data = data.get("users", [])
            return [User.from_dict(user_data) for user_data in users_data]

    def add(self, user: User):
        users = self.get_all()
        users.append(user)
        self._save_data(users)

    def delete(self, user_id: int):
        users = self.get_all()
        users = [user for user in users if user.user_id != user_id]
        self._save_data(users)

    def _save_data(self, users: List[User]):
        data = {"users": [user.to_dict() for user in users]}
        with open(self.file_path, "w") as file:
            json.dump(data, file)


class GroupChatJSONRepository(AbstractRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_by_id(self, group_chat_id: int) -> Optional[GroupChat]:
        group_chats = self.get_all()
        for group_chat in group_chats:
            if group_chat.group_chat_id == group_chat_id:
                return group_chat
        return None

    def get_all(self) -> List[GroupChat]:
        if os.stat(self.file_path).st_size == 0:
            return []
        with open(self.file_path, "r") as file:
            data = json.loads(file.read())
            group_chats_data = data.get("group_chats", [])
            return [GroupChat.from_dict(group_chat_data) for group_chat_data in group_chats_data]

    def add(self, group_chat: GroupChat):
        group_chats = self.get_all()
        group_chats.append(group_chat)
        self._save_data(group_chats)

    def delete(self, group_chat_id: int):
        group_chats = self.get_all()
        group_chats = [group_chat for group_chat in group_chats if group_chat.group_chat_id != group_chat_id]
        self._save_data(group_chats)

    def _save_data(self, group_chats: List[GroupChat]):
        data = {"group_chats": [group_chat.to_dict() for group_chat in group_chats]}
        with open(self.file_path, "w") as file:
            json.dump(data, file)


# XML Repositories

class UserXMLRepository(AbstractRepository):
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file, ET.XMLParser(encoding='utf-8'))
        self.root = self.tree.getroot()

    def get_by_id(self, user_id: int) -> Optional[User]:
        xpath_expr = f"./users/user[@user_id='{user_id}']"
        user_node = self.root.find(xpath_expr)
        if user_node is None:
            return None
        return self._node_to_user(user_node)

    def get_all(self) -> List[User]:
        users = []
        for user_node in self.root.findall('./users/user'):
            users.append(self._node_to_user(user_node))
        return users

    def add(self, user: User):
        users_node = self.root.find('./users')
        print(users_node)
        users_node.append(user.to_xml())
        self.tree.write(self.xml_file)

    def delete(self, user_id: int):
        parent_map = {c: p for p in self.tree.iter() for c in p}
        xpath_expr = f".//user[@user_id='{user_id}']"
        user_nodes = self.root.findall(xpath_expr)
        if user_nodes is not None:
            for user_node in user_nodes:
                parent_map[user_node].remove(user_node)
            self.tree.write(self.xml_file)

    def _node_to_user(self, user_node: ET.Element) -> User:
        user_id = int(user_node.get('user_id'))
        name = user_node.find('name').text
        email = user_node.find('email').text
        password = user_node.find('password').text

        return User(user_id, name, email, password)


class GroupChatXMLRepository(AbstractRepository):
    def __init__(self, xml_file: str, user_repository: UserXMLRepository):
        self.xml_file = xml_file
        self.user_repository = user_repository
        self.tree = ET.parse(xml_file, ET.XMLParser(encoding='utf-8'))
        self.root = self.tree.getroot()

    def get_by_id(self, group_chat_id: int) -> Optional[GroupChat]:
        xpath_expr = f"./group_chats/group_chat[@group_chat_id='{group_chat_id}']"
        group_chat_node = self.root.find(xpath_expr)
        if group_chat_node is None:
            return None
        return self._node_to_group_chat(group_chat_node)

    def get_all(self) -> List[GroupChat]:
        group_chats = []
        for group_chat_node in self.root.findall('group_chats/group_chat'):
            group_chats.append(self._node_to_group_chat(group_chat_node))
        return group_chats

    def add(self, group_chat: GroupChat):
        group_chats_node = self.root.find('./group_chats')
        group_chats_node.append(group_chat.to_xml())
        self.tree.write(self.xml_file)

        users_ids = []
        for member in group_chat.members:
            users_ids.append(member.user_id)

        print(users_ids)
        print('Это айдишки')

        users_nodes = []
        for user_id in users_ids:
            xpath = f"./users/user/[@user_id='{user_id}']"
            users_nodes.append(self.root.find(xpath))

        print(users_nodes)
        print('Это узлы найденные по айдишкам в XML')

        if not users_nodes:
            return False

        for user_node in users_nodes:
            group_chat_node = ET.Element('group_chat')
            group_chat_node.set('group_chat_id', str(group_chat.group_chat_id))
            user_node.find('./group_chats').append(group_chat_node)

        self.tree.write(self.xml_file)

    def delete(self, group_chat_id: int):
        xpath_expr = f".//group_chat[@user_id='{group_chat_id}']"
        group_chat_nodes = self.root.findall(xpath_expr)
        if group_chat_nodes is not None:
            for group_chat_node in group_chat_nodes:
                self.root.remove(group_chat_node)
                self.tree.write(self.xml_file)

    def _node_to_group_chat(self, group_chat_node: Element) -> GroupChat:
        group_chat_id = int(group_chat_node.get("group_chat_id"))
        name = group_chat_node.find("name").text

        members_nodes = group_chat_node.findall("members/member")
        members = [self.user_repository.get_by_id(int(member_node.get("user_id")))
                   for member_node in members_nodes]

        group_chat = GroupChat(group_chat_id, name, members)

        admins_nodes = group_chat_node.findall("admins/admin")
        group_chat.admins = [self.user_repository.get_by_id(int(admin_node.get("user_id")))
                             for admin_node in admins_nodes]

        # messages_nodes = group_chat_node.findall("messages/message")
        # group_chat.messages = [self._node_to_message(message_node, group_chat)
        #                        for message_node in messages_nodes]
        #
        # calls_nodes = group_chat_node.findall("calls/call")
        # group_chat.calls = [self._node_to_call(call_node, group_chat)
        #                     for call_node in calls_nodes]

        return group_chat


# SQLAlchemy Repositories


class UserSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> User:
        return self.session.query(models.User).filter_by(user_id=obj_id).first()

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def add(self, user: User):
        if self.get_by_id(user.user_id) is None:
            self.session.add(user)
            self.session.commit()

    def delete(self, obj_id: int):
        user = self.get_by_id(obj_id)
        if user is not None:
            self.session.delete(user)
            self.session.commit()


class GroupChatSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> GroupChat:
        return self.session.query(models.GroupChat).filter_by(group_chat_id=obj_id).first()

    def get_all(self) -> List[GroupChat]:
        return self.session.query(GroupChat).all()

    def add(self, group_chat: GroupChat):
        if self.get_by_id(group_chat.group_chat_id) is None:
            self.session.add(group_chat)
            self.session.commit()

    def delete(self, obj_id: int):
        group_chat = self.get_by_id(obj_id)
        if group_chat is not None:
            self.session.delete(group_chat)


class MessageSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> Message:
        return self.session.query(models.Message).filter_by(id=obj_id).first()

    def get_all(self) -> List[Message]:
        return self.session.query(Message).all()

    def add(self, message: Message):
        self.session.add(message)
        self.session.commit()

    def delete(self, obj_id: int):
        message = self.get_by_id(obj_id)
        if message is not None:
            self.session.delete(message)


# FakeRepositories

class UserLocalRepository(AbstractRepository):
    def __init__(self):
        self.users: List[User] = []

    def get_by_id(self, obj_id: int):
        for user in self.users:
            if user.user_id == obj_id:
                return user
        return None

    def get_all(self):
        return self.users

    def add(self, user: User):
        self.users.append(user)

    def delete(self, obj_id: int):
        user = self.get_by_id(obj_id)
        if user is not None:
            self.users.remove(user)


class MessageLocalRepository(AbstractRepository):
    def __init__(self):
        self.messages: List[Message] = []

    def get_by_id(self, obj_id: int):
        for message in self.messages:
            if message.message_id == obj_id:
                return message
        return None

    def get_all(self):
        return self.messages

    def add(self, message: Message):
        self.messages.append(message)

    def delete(self, obj_id: int):
        message = self.get_by_id(obj_id)
        if message is not None:
            self.messages.remove(message)


class GroupChatLocalRepository(AbstractRepository):
    def __init__(self):
        self.group_chats: List[GroupChat] = []

    def get_by_id(self, obj_id: int):
        for group_chat in self.group_chats:
            if group_chat.group_chat_id == obj_id:
                return group_chat
        return None

    def get_all(self):
        return self.group_chats

    def add(self, group_chat: GroupChat):
        self.group_chats.append(group_chat)

    def delete(self, obj_id: int):
        group_chat = self.get_by_id(obj_id)
        if group_chat is not None:
            self.group_chats.remove(group_chat)
