from .cloudcms_object import CloudCMSObject
from .repository import Repository

class Platform(CloudCMSObject):

    def __init__(self, client, data):
        super(Platform, self).__init__(client, data)

    def uri(self):
        return ''

    def list_repositories(self):
        uri = self.uri() + '/repositories'
        res = self.client.get(uri)
        return Repository.repository_map(self.client, res['rows'])

    def read_repository(self, repository_id):
        res = self.client.get('/repositories/' + repository_id)
        return Repository(self.client, res)