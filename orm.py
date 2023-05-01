from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, MetaData, Boolean, Text
from sqlalchemy.orm import registry, relationship
import models

metadata = MetaData()
mapper_registry = registry()

# таблица пользователя
users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True, autoincrement=False),
              Column('name', String),
              Column('email', String),
              Column('password', String)
              )

# таблица групповых чатов
group_chats = Table('group_chats', metadata,
                    Column('group_chat_id', Integer, primary_key=True, autoincrement=False),
                    Column('name', String),
                    Column('creator_id', Integer, ForeignKey('users.user_id')),
                    )

# таблица многие-ко-многим Пользователь-Чат
group_chat_members = Table('members', metadata,
                           Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
                           Column('group_chat_id', Integer, ForeignKey('group_chats.group_chat_id'), primary_key=True),
                           Column('is_admin', Boolean, default=False)
                           )

# таблица с сообщениями
messages = Table('messages', metadata,
                 Column('message_id', Integer, primary_key=True, autoincrement=False),
                 Column('sender_id', Integer, ForeignKey('users.user_id')),
                 Column('group_chat_id', Integer, ForeignKey('group_chats.group_chat_id')),
                 Column('text', String),
                 Column('video_ref', String),
                 Column('image_ref', String),
                 Column('timestamp', DateTime)
                 )


def start_mappers():
    mapper_registry.map_imperatively(models.User, users, properties={
        'group_chats': relationship(models.GroupChat, secondary=group_chat_members)
    })

    mapper_registry.map_imperatively(models.GroupChat, group_chats, properties={
        'members': relationship(models.User, secondary=group_chat_members),
        'messages': relationship(models.Message),
    })

    mapper_registry.map_imperatively(models.Message, messages, properties={
        'sender': relationship(models.User),
        'group_chat': relationship(models.GroupChat)
    })
