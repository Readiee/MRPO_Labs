import repositories
import services
import unit_of_work
from models import *

uow = unit_of_work.SqlAlchemyUnitOfWork()
# uow = unit_of_work.XMLUnitOfWork()
# uow = unit_of_work.JSONUnitOfWork()


def test_creates_user():
    name = 'Bulat'
    email = 'buladat1@mail.ru'
    password = 'qwerty213'

    with uow:
        before_count = len(uow.users.get_all())

    services.create_user(uow, name, email, password)

    with uow:
        assert len(uow.users.get_all()) == before_count + 1


def test_creates_group_chat():
    group_chat_name = 'GroupChat123'
    user1_id = services.create_user(uow, 'Alina', 'alina23@mail.ru', 'eriiir2')
    user2_id = services.create_user(uow, 'Stepan', 'stepan33@mail.ru', 'stem221')

    with uow:
        before_count = len(uow.group_chats.get_all())
        members = [uow.users.get_by_id(user1_id), uow.users.get_by_id(user2_id)]

    services.create_group_chat(uow, group_chat_name, members)

    with uow:
        assert len(uow.group_chats.get_all()) == before_count + 1
        assert uow.group_chats.get_all()[-1].members[-1].name == 'Stepan'


