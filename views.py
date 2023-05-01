import unit_of_work


def get_user_by_id(user_id: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        user = uow.users.get_by_id(user_id)
        uow.session.expunge(user)
        return user.to_dict()


def get_users(uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        users = uow.users.get_all()
        for user in users:
            uow.session.expunge(user)
        return [user.to_dict() for user in users]

def get_group_chat_by_id(group_chat_id: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        group_chat = uow.group_chats.get_by_id(group_chat_id)
        uow.session.expunge(group_chat)
        return group_chat.to_dict()


def get_group_chats(uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        group_chats = uow.group_chats.get_all()
        for group_chat in group_chats:
            uow.session.expunge(group_chat)
        return [group_chat.to_dict() for group_chat in group_chats]
