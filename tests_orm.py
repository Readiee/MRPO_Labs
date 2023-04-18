from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import repositories
import orm

engine = create_engine('postgresql://postgres:root@localhost:5432/mrpo')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

orm.metadata.create_all(bind=engine)
orm.start_mappers()


def test_user_repository_can_save_user():
    users_repo = repositories.UserSQLAlchemyRepository(session)
    new_user_id = 12
    new_user = models.User(user_id=new_user_id, name="Булат", email="bulat@mail.ru", password="bqwerty123")

    before_count = len(users_repo.get_all())
    # Если пользователя нет в репозитории
    if users_repo.get_by_id(new_user_id) is None:
        users_repo.add(new_user)
        # +1 пользователь
        assert len(users_repo.get_all()) == before_count + 1
        assert new_user == users_repo.get_by_id(new_user_id)
    # Если пользователь уже есть в репозитории
    else:
        users_repo.add(new_user)
        # ничего не меняется
        assert len(users_repo.get_all()) == before_count


def test_user_repository_can_delete_user():
    users_repo = repositories.UserSQLAlchemyRepository(session)
    user_id = 222
    user = models.User(user_id, "Алина", "alina@mail.ru", "aqwerty123")
    users_repo.add(user)
    before_count = len(users_repo.get_all())
    users_repo.delete(user_id)
    assert before_count - 1 == len(users_repo.get_all())
    assert users_repo.get_by_id(user_id) is None


def test_repository_can_save_group_chat():
    group_chats_repo = repositories.GroupChatSQLAlchemyRepository(session)
    users_repo = repositories.UserSQLAlchemyRepository(session)
    user_1 = models.User(43, "Данил", "danil@mail.ru", "dqwerty123")
    user_2 = models.User(78, "Анастасия", "anastasia@mail.ru", "anqwerty123")
    users_repo.add(user_1)
    users_repo.add(user_2)

    new_group_chat_id = 555
    members = [users_repo.get_by_id(43), users_repo.get_by_id(78)]
    new_group_chat = models.GroupChat(new_group_chat_id, 'WorkChat', members)

    before_count = len(group_chats_repo.get_all())
    # Если группового чата еще нет в репозитории:
    if group_chats_repo.get_by_id(new_group_chat.group_chat_id) is None:
        group_chats_repo.add(new_group_chat)
        models.make_admin_of_group_chat(new_group_chat.members[0], new_group_chat)
        # + 1 групповой чат
        assert before_count + 1 == len(group_chats_repo.get_all())
        # assert group_chats_repo.get_by_id(new_group_chat_id).members[1].name == 'Анастасия'
        # assert group_chats_repo.get_by_id(new_group_chat_id).creator.name == 'Данил'
    # Если групповой чат уже есть в репозитории:
    else:
        group_chats_repo.add(new_group_chat)
        # ничего не меняется
        assert before_count == len(group_chats_repo.get_all())



