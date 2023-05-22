from repositories import UserXMLRepository, UserJSONRepository


class RepositoryFactory:
    def create_repository(self, format):
        repo_creator = get_repo_creator(format)
        return repo_creator()


def get_repo_creator(format):
    if format == 'JSON':
        return _create_repository_json
    elif format == 'XML':
        return _create_repository_xml
    else:
        raise ValueError(format)


def _create_repository_json():
    return UserJSONRepository('mrpo_users.json')

def _create_repository_xml():
    return UserXMLRepository('mrpo.xml')

# Tests
def test_can_create_json_repo():
    factory = RepositoryFactory()
    repo = factory.create_repository('JSON')
    assert isinstance(repo, UserJSONRepository)

def test_can_create_json_repo():
    factory = RepositoryFactory()
    repo = factory.create_repository('XML')
    assert isinstance(repo, UserXMLRepository)

