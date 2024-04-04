import mongomock
from ..directory import Directory
from notebox.shared.directory import Directory
from notebox.shared.file import File
from datetime import datetime, timedelta

import unittest

class TestDirectory(unittest.TestCase):
    def setUp(self):
        yesterday = datetime.now() - timedelta(days=1)
        twoHoursAgo = datetime.now() - timedelta(hours=2)
        self.today = twoHoursAgo.timestamp()
        self.yesterday = yesterday.timestamp()
        self.dir = Directory("/test/path", [File("/test/path/a", self.yesterday), File("/test/path/b", self.yesterday)])
    

    def test_returns_new_files(self):
        directory = Directory("/test/path", [File("/test/path/a", self.yesterday), File("/test/path/c", self.yesterday)])

        returned = self.dir.getChanges(directory)

        self.assertEqual(len(returned["newFiles"]), 1)
        self.assertEqual(str(returned["newFiles"][0]), str(directory.files[1]))
    
    def test_returns_modified_files(self):
        directory = Directory("/test/path", [File("/test/path/a", self.yesterday), File("/test/path/b", self.today)])

        returned = self.dir.getChanges(directory)

        self.assertEqual(len(returned["modifiedFiles"]), 1)
        self.assertEqual(str(returned["modifiedFiles"][0]), str(directory.files[1]))

    def test_returns_deleted_files(self):
        directory = Directory("/test/path", [File("/test/path/a", self.yesterday)])

        returned = self.dir.getChanges(directory)

        self.assertEqual(len(returned["deletedFiles"]), 1)
        self.assertEqual(str(returned["deletedFiles"][0]), str(self.dir.files[1]))

    def test_no_changes(self):
        directory = Directory("/test/path", [File("/test/path/a", self.yesterday), File("/test/path/b", self.yesterday)])

        returned = self.dir.getChanges(directory)

        self.assertEqual(len(returned["deletedFiles"]),0)
        self.assertEqual(len(returned["modifiedFiles"]), 0)
        self.assertEqual(len(returned["newFiles"]), 0)

    def test_multiple_changes(self):
        directory = Directory("/test/path", [File("/test/path/a", self.today), File("/test/path/c", self.yesterday)])

        returned = self.dir.getChanges(directory)

        self.assertEqual(len(returned["deletedFiles"]),1)
        self.assertEqual(len(returned["modifiedFiles"]), 1)
        self.assertEqual(len(returned["newFiles"]), 1)
        self.assertEqual(str(returned["modifiedFiles"][0]), str(directory.files[0]))
        self.assertEqual(str(returned["deletedFiles"][0]), str(self.dir.files[1]))
        self.assertEqual(str(returned["newFiles"][0]), str(directory.files[1]))


if __name__ == '__main__':
    unittest.main()