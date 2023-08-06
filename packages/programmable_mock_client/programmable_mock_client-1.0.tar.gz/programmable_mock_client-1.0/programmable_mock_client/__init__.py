import requests

class ProgrammableMockClient:
    def __init__(self, options):
        self.url = options['url']
        self.tricks = []
        self.rules = []

    def onRequest(self, reqDef):
        self.rules.append({ 'reqDef': reqDef })
        return self

    def respondWith(self, resDef):
        self.rules[len(self.rules) - 1]['resDef'] = resDef
        return self

    def save(self):
        requests.post(self.url + '/internal/api/v1/batchMock', json=self.rules)
        self.rules = []
        return self

    @staticmethod
    def createMock(options):
        return ProgrammableMockClient(options)
