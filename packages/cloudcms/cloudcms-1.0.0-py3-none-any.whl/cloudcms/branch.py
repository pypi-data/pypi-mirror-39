import json
from .repository_object import RepositoryObject
from .node import Node

class Branch(RepositoryObject):

    def __init__(self, repository, data):
        super(Branch, self).__init__(repository, data)

    def uri(self):
        return '%s/branches/%s' % (self.repository.uri(), self._doc) 

    def read_node(self, node_id):
        uri = self.uri() + "/nodes/" + node_id
        res = self.client.get(uri)

        return Node(self, res)
    
    def query_nodes(self, query, pagination={}):
        uri = self.uri() + "/nodes/query"

        res = self.client.post(uri, params=pagination, data=query)
        return Node.node_map(self, res['rows'])

    def find_nodes(self, config, pagination={}):
        uri = self.uri() + "/nodes/find"

        res = self.client.post(uri, params=pagination, data=config)
        return Node.node_map(self, res['rows'])

    def create_node(self, obj, options={}):
        uri = self.uri() + "/nodes"

        params = {}
        params['rootNodeId'] = options.get('rootNodeId') or 'root'
        params['associationType'] = options.get('associationType') or 'a:child'

        if 'parentFolderPath' in options:
            params['parentFolderPath'] = options['parentFolderPath']
        elif 'folderPath' in options:
            params['parentFolderPath'] = options['folderPath']
        elif 'folderpath' in options:
            params['parentFolderPath'] = options['folderpath']  
        
        if 'filePath' in options:
            params['filePath'] = options['filePath']
        elif 'filepath' in options:
            params['filePath'] = options['filepath']

        res = self.client.post(uri, params=params, data=obj)
        return res['_doc']

    def delete_nodes(self, nodeIds):
        uri = self.uri() + '/nodes/delete'
        return self.client.post(uri, data=nodeIds)

    @classmethod
    def branch_map(cls, repository, data):
        return {branch['_doc']: Branch(repository, branch) for branch in data}