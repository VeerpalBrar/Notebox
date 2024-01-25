import elasticsearch
from ..shared.settings import config

class ElasticClient:
    def __init__(self, client=None, index = config["INDEX"]):
        if client != None:
            self.client = client
        else:
            self.client =  elasticsearch.Elasticsearch(
                config["ELASTIC_SEARCH_HOST"],  # Elasticsearch endpoint
                ssl_assert_fingerprint=config["CERT_FINGERPRINT"],
                basic_auth=(config["ELASTIC_SEARCH_USER"], config["ELASTIC_SEARCH_PASSWORD"]),  
            )
        self.index = index
    
    def search(self, content):
        response = self.client.search(index=self.index, query={
            "match": {
                "content": content
            }
        })

        print(response)

        return list(map(self.convert_to_hash, response['hits']['hits']))
    
    
    def updateDocument(self, id, content):
        response = self.client.update(index=self.index, id=id, doc={
            "content": content
        })

        return response
    
    def createDocument(self, id, content):
        response = self.client.index(index=self.index, id=id, document={
            "content": content
        })

        return response 

    def getDocument(self, id):
        response = self.client.get(index=self.index, id=id)

        return self.convert_to_hash(response)
    
    def deleteDocument(self, id):
        response = self.client.delete(index=self.index, id=id)
        return response

    def convert_to_hash(self, f):
            return {
                "path": f["_id"],
                "content": f["_source"]["content"]
            }

# print(ElasticClient().search("substack"))