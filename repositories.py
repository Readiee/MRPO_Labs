from abc import ABC, abstractmethod

from sqlalchemy import text

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


class UserSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, obj_id: int) -> User:
        return self.session.query(models.User).filter_by(id=obj_id).first()

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def add(self, user: User):
        if self.get_by_id(user.user_id) is None:
            self.session.execute(text(
                f"INSERT INTO users (id, name, email, password) VALUES ('{user.user_id}', '{user.name}', '{user.email}', '{user.password}')"))
            # self.session.add(user) - НЕ РАБОТАЕТ
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
        return self.session.query(models.GroupChat).filter_by(id=obj_id).first()

    def get_all(self) -> List[GroupChat]:
        return self.session.query(GroupChat).all()

    def add(self, group_chat: GroupChat):
        if self.get_by_id(group_chat.group_chat_id) is None:
            # self.session.add(group_chat) - Не работает =(
            self.session.execute(text(
                f"INSERT INTO group_chats (id, name) VALUES ('{group_chat.group_chat_id}', '{group_chat.name}')"))
            # for member in group_chat.members:
            #     self.session.execute(text(
            #         f"INSERT INTO group_chat_members (user_id, group_chat_id, is_admin) VALUES ('{len(member.name) * 2}', '{group_chat.group_chat_id}', 'False')"))
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
