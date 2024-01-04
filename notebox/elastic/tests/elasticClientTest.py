from ..elasticClient import ElasticClient
from ...shared.settings import config
import elasticsearch


INDEX = "documents-test"

import unittest

class TestElasticClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.elastic_search = elasticsearch.Elasticsearch(
                config["ELASTIC_SEARCH_HOST"],  # Elasticsearch endpoint
                ssl_assert_fingerprint=config["CERT_FINGERPRINT"],
                basic_auth=(config["ELASTIC_SEARCH_USER"], config["ELASTIC_SEARCH_PASSWORD"]),  
            )
        cls.elastic_search.indices.create(index=INDEX, ignore=400)
        
    @classmethod    
    def tearDownClass(cls):
        # Teardown: Clean up resources after the test session
        cls.elastic_search.indices.delete(index=INDEX, ignore=[400, 404])


    def test_create_and_get_document(self):
        es_client = ElasticClient(self.elastic_search, INDEX)
        
        # Index a document
        doc_id = "test_document"
        content = "title\nline"
        create_response = es_client.createDocument(id=doc_id, content=content)

        # Assert that the document was created successfully
        assert create_response["result"] == "created"

        # Get the created document
        get_response = es_client.getDocument(id=doc_id)

        # Assert that the retrieved document matches the created document
        assert get_response["_id"] == doc_id
        assert get_response["_source"]["content"] == content


    def test_update_document(self):
        # Create an instance of ElasticClient
        es_client = ElasticClient(self.elastic_search, INDEX)
        
        # Index a document
        doc_id = "test_document"
        content = "title\nline"
        es_client.createDocument(id=doc_id, content=content)

        # Update the document
        updated_content = "title\nline\nupdated"
        es_client.updateDocument(id=doc_id, content=updated_content)


        # Get the updated document
        get_response = es_client.getDocument(id=doc_id)

        # Assert that the retrieved document matches the updated content
        assert get_response["_id"] == doc_id
        assert get_response["_source"]["content"] == updated_content


    def test_delete_document(self):
        # Create an instance of ElasticClient
        es_client = ElasticClient(self.elastic_search, INDEX)
        
        # Index a document
        doc_id = "test_document"
        content = "title\nline"
        es_client.createDocument(id=doc_id, content=content)

        # Delete the document
        delete_response = es_client.deleteDocument(id=doc_id)

        # Assert that the document was deleted successfully
        assert delete_response["result"] == "deleted"

        # Try to get the deleted document
        self.assertRaises(elasticsearch.NotFoundError, es_client.getDocument, doc_id)


if __name__ == '__main__':
    unittest.main()