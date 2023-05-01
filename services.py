from typing import List

import models
import unit_of_work


def create_user(
        uow: unit_of_work.AbstractUnitOfWork,
        name: str,
        email: str,
        password: str
):
    with uow:
        # for user in uow.users.get_all():
        #     if user.email == email:
        #         return 'Email is already used by other user.'
        max_id = 0
        for user in uow.users.get_all():
            if user.user_id > max_id:
                max_id = user.user_id
        user_id = max_id + 1

        user = models.create_user(user_id, name, email, password)
        uow.users.add(user)
        uow.commit()
        return uow.users.get_by_id(user_id).user_id


def create_group_chat(
        uow: unit_of_work.AbstractUnitOfWork,
        name: str,
        members: List[models.User]
):
    with uow:
        if members is None:
            return None
        max_id = 0
        for group_chat in uow.group_chats.get_all():
            if group_chat.group_chat_id > max_id:
                max_id = group_chat.group_chat_id
        group_chat_id = max_id + 1

        group_chat = models.create_group_chat(group_chat_id, name, members)
        uow.group_chats.add(group_chat)

        uow.commit()
        return uow.group_chats.get_by_id(group_chat_id)
