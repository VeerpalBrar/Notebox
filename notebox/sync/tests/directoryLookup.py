import mongomock
from ..directoryLookup import DirectoryLookup
from notebox.shared.directory import Directory
from notebox.shared.file import File
from datetime import datetime, timedelta

import unittest

class TestDirectoryLookup(unittest.TestCase):
    def setUp(self):
        self.mongo = mongomock.MongoClient().db.collection
        yesterday = datetime.now() - timedelta(days=1)
        self.yesterday = yesterday.timestamp()
        

    def test_updates_directory(self):
        directory = Directory("/test/path", [File("/test/path/a", self.yesterday)])

        lookup = DirectoryLookup(self.mongo)
        lookup.save(directory)

        returned = lookup.getStoredDirectoryContents("/test/path")

        self.assertEqual(str(returned), str(directory))
    
    def returns_empty_directory_if_directory_does_not_exist(self):
        directory = Directory("/test/path", [File("/test/path/a", self.yesterday)])

        lookup = DirectoryLookup(self.mongo)
        lookup.save(directory)

        returned = lookup.getStoredDirectoryContents("/test/path/b")

        self.assertEqual(returned, Directory("/test/path/b", []))

if __name__ == '__main__':
    unittest.main()