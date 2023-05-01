import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import orm
import repositories


class AbstractUnitOfWork(abc.ABC):
    users: repositories.AbstractRepository
    group_chats: repositories.AbstractRepository
    messages: repositories.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


engine = create_engine('postgresql://postgres:root@localhost:5432/mrpo')
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=engine,
    isolation_level="REPEATABLE READ",
    expire_on_commit=False
)
orm.metadata.create_all(bind=engine)
orm.start_mappers()


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        self.session = session
        self.users = repositories.UserSQLAlchemyRepository(self.session)
        self.group_chats = repositories.GroupChatSQLAlchemyRepository(self.session)
        self.messages = repositories.MessageSQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


DEFAULT_XML_FILE_PATH = 'mrpo.xml'


class XMLUnitOfWork(AbstractUnitOfWork):
    def __init__(self, file_path=DEFAULT_XML_FILE_PATH):
        self.file_path = file_path

    def __enter__(self):
        self.xml_file = self.file_path
        self.users = repositories.UserXMLRepository(self.xml_file)
        self.group_chats = repositories.GroupChatXMLRepository(self.xml_file, self.users)
        # self.messages = repositories.MessageXmlRepository(self.file_path, self.users, self.group_chats)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        pass

    def rollback(self):
        pass


DEFAULT_JSON_FILE_PATH_USERS = 'mrpo_users.json'
DEFAULT_JSON_FILE_PATH_GROUP_CHATS = 'mrpo_group_chats.json'


class JSONUnitOfWork(AbstractUnitOfWork):
    def __init__(
            self,
            users_file_path=DEFAULT_JSON_FILE_PATH_USERS,
            group_chats_file_path=DEFAULT_JSON_FILE_PATH_GROUP_CHATS
    ):
        self.users_file_path = users_file_path
        self.group_chats_file_path = group_chats_file_path

    def __enter__(self):
        self.users_json = self.users_file_path
        self.group_chats_json = self.group_chats_file_path

        self.users = repositories.UserJSONRepository(self.users_json)
        self.group_chats = repositories.GroupChatJSONRepository(self.group_chats_json)
        # self.messages =
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        pass

    def rollback(self):
        pass
