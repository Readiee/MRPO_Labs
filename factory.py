from repositories import UserXMLRepository, UserJSONRepository

class RepositoryFactory:
    def create_repo(self, format):
        repo_creator = get_repo_creator(format)
        return repo_creator()


def get_repo_creator(format):
    if format == 'JSON':
        return _create_repo_json
    elif format == 'XML':
        return _create_repo_xml
    else:
        raise ValueError(format)


def _create_repo_json():
    return UserJSONRepository('mrpo_users.json')

def _create_repo_xml():
    return UserXMLRepository('mrpo.xml')
