class CloudCMSObject:
    
    def __init__(self, client, data):
        self.client = client
        self._doc = data['_doc']

        self.data = data

    def uri(self):
        raise NotImplementedError()

    def reload(self):
        self.data = self.client.get(self.uri())

    def delete(self):
        return self.client.delete(self.uri())

    def update(self):
        return self.client.put(self.uri(), data=self.data)