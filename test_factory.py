from repositories import UserXMLRepository, UserJSONRepository
from factory import RepositoryFactory

def test_can_create_json_repo():
    factory = RepositoryFactory()
    repo = factory.create_repo('JSON')
    assert isinstance(repo, UserJSONRepository)

def test_can_create_xml_repo():
    factory = RepositoryFactory()
    repo = factory.create_repo('XML')
    assert isinstance(repo, UserXMLRepository)


