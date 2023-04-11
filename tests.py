from models import User, Message, GroupChat, Content
from repositories import UserLocalRepository, GroupChatLocalRepository, MessageLocalRepository
from services import *


# Создать пользователя
def test_local_repo_user_service_can_create_user():
    user = create_user('Булат', 'pochta@mail.ru', 'qwerty1234')
    assert isinstance(user, User)
    assert user.name == 'Булат'


# Создать групповой чат
def test_local_repo_group_chat_service_can_create_chat():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    member3 = create_user('Евгений', 'zheka@mail.ru', 'zheka2003')
    chat_members = [member1, member2, member3]

    created_group_chat = create_group_chat('Рабочий чат', chat_members)
    assert isinstance(created_group_chat, GroupChat)
    # Указан создатель(креатор)
    assert created_group_chat.creator.name == 'Булат'


# Добавить пользователя в чат
def test_local_repo_group_chat_service_can_add_user_to_chat():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    member3 = create_user('Евгений', 'zheka@mail.ru', 'zheka2003')
    chat_members = [member1, member2]
    group_chat = create_group_chat('Рабочий чат', chat_members)

    # Нельзя добавить, если пользователь уже есть в чате
    assert len(group_chat.members) == 2
    add_user_to_group_chat(member1, group_chat)
    assert len(group_chat.members) == 2

    # Можно добавить, если пользователя нет в чате
    add_user_to_group_chat(member3, group_chat)
    assert len(group_chat.members) == 3
    assert group_chat.members[2].name == 'Евгений'


# Удалить пользователя из группового чата
def test_local_repo_group_chat_service_can_remove_user_from_chat():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    member3 = create_user('Евгений', 'zheka@mail.ru', 'zheka2003')

    group_chat = create_group_chat('Рабочий чат', [member1, member2])

    # Нельзя удалить, если пользователя нет в чате
    assert len(group_chat.members) == 2
    remove_user_from_group_chat(member3, group_chat)
    assert len(group_chat.members) == 2

    # Можно удалить, если пользователь есть в чате
    remove_user_from_group_chat(member2, group_chat)
    assert len(group_chat.members) == 1


# Назначить пользователя администратором группы
def test_local_repo_group_chat_service_can_make_admin():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    member3 = create_user('Евгений', 'zheka@mail.ru', 'zheka2003')
    group_chat = create_group_chat('Рабочий чат', [member1, member2])

    # Нельзя назначить, если нет в чате
    make_admin_of_group_chat(member3, group_chat)
    assert member3 not in group_chat.admins

    # Нельзя назначить, если является создателем (владельцем)
    assert group_chat.creator == member1
    make_admin_of_group_chat(member1, group_chat)
    assert member1 not in group_chat.admins

    # Можно назначить, если есть в беседе и не является администратором и создателем
    assert member2 not in group_chat.admins
    make_admin_of_group_chat(member2, group_chat)
    assert member2 in group_chat.admins

    # Нельзя назначить, если уже является администратором
    admins_num_before_method = len(group_chat.admins)
    make_admin_of_group_chat(member2, group_chat)
    admins_num_after_method = len(group_chat.admins)
    assert admins_num_after_method == admins_num_before_method


# Отправить сообщение в чат
def test_local_repo_message_service_can_send_message():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    group_chat = create_group_chat('Рабочий чат', [member1, member2])

    # Объект-значение, хы
    content = Content('Привет', 'image-ref-3123', 'video-ref-8481')

    # Нет сообщений в репозитории и в чате до выполнения метода
    assert len(group_chat.messages) == 0
    send_message(member1, group_chat, content)
    # Есть сообщения в репозитории и в чате после выполнения метода
    assert group_chat.messages[0].content.text == 'Привет'


# Удалить сообщение
def test_local_repo_message_service_can_delete_message():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    group_chat_1 = create_group_chat('Рабочий чат', [member1, member2])
    group_chat_2 = create_group_chat('НЕ рабочий чат', [member1, member2])

    # Объект-значение, хы
    content = Content('Привет', 'image-ref-3123', 'video-ref-8481')

    # Отправили сообщение в чат 1
    send_message(member1, group_chat_1, content)

    # Нельзя удалить, если сообщения нет в чате (Пытаемся удалить из чата 2)
    delete_message(group_chat_1.messages[0], group_chat_2)
    assert len(group_chat_1.messages) == 1

    # Можно удалить, если есть сообщение в чате (Удаляем из чата 1)
    delete_message(group_chat_1.messages[0], group_chat_1)
    assert len(group_chat_1.messages) == 0


# Найти сообщения по тексту
def test_local_repo_message_service_can_find_messages_by_text():
    member1 = create_user('Булат', 'bulat@mail.ru', 'bulat2003')
    member2 = create_user('Анна', 'anna@mail.ru', 'anna2003')
    group_chat = create_group_chat('Рабочий чат', [member1, member2])

    # Отправляем сообщения в чат
    send_message(member1, group_chat, Content('Привет', 'img-ref', 'vid-ref'))
    send_message(member1, group_chat, Content('Привет1234', 'img-ref', 'vid-ref'))
    send_message(member1, group_chat, Content('Здрасьте', 'img-ref', 'vid-ref'))

    # Находит сообщения, если такие есть
    found_messages = find_messages_by_text('Привет', group_chat)
    assert len(found_messages) == 2

    # Не находит сообщения, если таких нет
    found_messages = find_messages_by_text('Блабла', group_chat)
    assert len(found_messages) == 0
