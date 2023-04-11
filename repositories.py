from abc import ABC, abstractmethod
from models import *


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, obj_id: str):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def delete(self, obj_id: str):
        pass


class UserLocalRepository(AbstractRepository):
    def __init__(self):
        self.users: List[User] = []

    def get_by_id(self, obj_id: str):
        for user in self.users:
            if user.user_id == obj_id:
                return user
        return None

    def get_all(self):
        return self.users

    def add(self, user: User):
        self.users.append(user)

    def delete(self, obj_id: str):
        user = self.get_by_id(obj_id)
        if user is not None:
            self.users.remove(user)


class MessageLocalRepository(AbstractRepository):
    def __init__(self):
        self.messages: List[Message] = []

    def get_by_id(self, obj_id: str):
        for message in self.messages:
            if message.message_id == obj_id:
                return message
        return None

    def get_all(self):
        return self.messages

    def add(self, message: Message):
        self.messages.append(message)

    def delete(self, obj_id: str):
        message = self.get_by_id(obj_id)
        if message is not None:
            self.messages.remove(message)


class GroupChatLocalRepository(AbstractRepository):
    def __init__(self):
        self.group_chats: List[GroupChat] = []

    def get_by_id(self, obj_id: str):
        for group_chat in self.group_chats:
            if group_chat.group_chat_id == obj_id:
                return group_chat
        return None

    def get_all(self):
        return self.group_chats

    def add(self, group_chat: GroupChat):
        self.group_chats.append(group_chat)

    def delete(self, obj_id: str):
        group_chat = self.get_by_id(obj_id)
        if group_chat is not None:
            self.group_chats.remove(group_chat)

# class AbstractUserRepository(ABC):
#     @abstractmethod
#     def get_user_by_id(self, user_id: str) -> User:
#         pass
#
#     @abstractmethod
#     def get_all_users(self) -> List[User]:
#         pass
#
#     @abstractmethod
#     def add_user(self, user: User):
#         pass
#
#     @abstractmethod
#     def delete_user(self, user_id: str):
#         pass
#
# class AbstractMessageRepository(ABC):
#     @abstractmethod
#     def get_message_by_id(self, message_id: str) -> Message:
#         pass
#
#     @abstractmethod
#     def get_all_messages(self) -> List[Message]:
#         pass
#
#     @abstractmethod
#     def add_message(self, message: Message):
#         pass
#
#     @abstractmethod
#     def delete_message(self, message_id: str):
#         pass
#
# class AbstractGroupChatRepository(ABC):
#     @abstractmethod
#     def get_group_chat_by_id(self, group_chat_id: str) -> GroupChat:
#         pass
#
#     @abstractmethod
#     def get_all_group_chats(self) -> List[GroupChat]:
#         pass
#
#     @abstractmethod
#     def add_group_chat(self, group_chat: GroupChat):
#         pass
#
#     @abstractmethod
#     def delete_group_chat(self, group_chat_id: str):
#         pass
#
# class AbstractPersonalChatRepository(ABC):
#     @abstractmethod
#     def get_personal_chat_by_id(self, personal_chat_id: str) -> PersonalChat:
#         pass
#
#     @abstractmethod
#     def get_all_personal_chats(self) -> List[PersonalChat]:
#         pass
#
#     @abstractmethod
#     def add_personal_chat(self, personal_chat: PersonalChat):
#         pass
#
#     @abstractmethod
#     def delete_personal_chat(self, personal_chat_id: str):
#         pass
#
# class AbstractCallRepository(ABC):
#     @abstractmethod
#     def get_call_by_id(self, call_id: str) -> Call:
#         pass
#
#     @abstractmethod
#     def get_all_calls(self) -> List[Call]:
#         pass
#
#     @abstractmethod
#     def add_call(self, call: Call):
#         pass
#
#     @abstractmethod
#     def delete_call(self, call_id: str):
#         pass
#
#
# class UserLocalRepository(AbstractUserRepository):
#     def __init__(self):
#         self.users: List[User] = []
#
#     def get_user_by_id(self, user_id: str):
#         for user in self.users:
#             if user.user_id == user_id:
#                 return user
#         return None
#
#     def get_all_users(self):
#         return self.users
#
#     def add_user(self, user):
#         self.users.append(user)
#
#     def delete_user(self, user_id: str):
#         for user in self.users:
#             if user.user_id == user_id:
#                 self.users.remove(user)
#                 return
#
# class MessageLocalRepository(AbstractMessageRepository):
#     def __init__(self):
#         self.messages: List[Message] = []
#
#     def get_message_by_id(self, message_id: str):
#         for message in self.messages:
#             if message.message_id == message_id:
#                 return message
#         return None
#
#     def get_all_messages(self):
#         return self.messages
#
#     def add_message(self, message):
#         self.messages.append(message)
#
#     def delete_message(self, message_id: str):
#         for message in self.messages:
#             if message.message_id == message_id:
#                 self.messages.remove(message)
#                 return
#
# class GroupChatLocalRepository(AbstractGroupChatRepository):
#     def __init__(self):
#         self.group_chats: List[GroupChat] = []
#
#     def get_group_chat_by_id(self, group_chat_id: str):
#         for group_chat in self.group_chats:
#             if group_chat.group_chat_id == group_chat_id:
#                 return group_chat
#         return None
#
#     def get_all_group_chats(self):
#         return self.group_chats
#
#     def add_group_chat(self, group_chat):
#         self.group_chats.append(group_chat)
#
#     def delete_group_chat(self, group_chat_id: str):
#         for group_chat in self.group_chats:
#             if group_chat.group_chat_id == group_chat_id:
#                 self.group_chats.remove(group_chat)
#                 return
#
# class PersonalChatLocalRepository(AbstractPersonalChatRepository):
#     def __init__(self):
#         self.personal_chats: List[PersonalChat] = []
#
#     def get_personal_chat_by_id(self, personal_chat_id: str):
#         for personal_chat in self.personal_chats:
#             if personal_chat.personal_chat_id == personal_chat_id:
#                 return personal_chat
#         return None
#
#     def get_all_personal_chats(self):
#         return self.personal_chats
#
#     def add_personal_chat(self, personal_chat):
#         self.personal_chats.append(personal_chat)
#
#     def delete_personal_chat(self, personal_chat_id: str):
#         for personal_chat in self.personal_chats:
#             if personal_chat.personal_chat_id == personal_chat_id:
#                 self.personal_chats.remove(personal_chat)
#                 return
#
# class CallLocalRepository(AbstractCallRepository):
#     def __init__(self):
#         self.calls: List[Call] = []
#
#     def get_call_by_id(self, call_id: str):
#         for call in self.calls:
#             if call.call_id == call_id:
#                 return call
#         return None
#
#     def get_all_calls(self):
#         return self.calls
#
#     def add_call(self, call):
#         self.calls.append(call)
#
#     def delete_call(self, call_id: str):
#         for call in self.calls:
#             if call.call_id == call_id:
#                 self.calls.remove(call)
#                 return
