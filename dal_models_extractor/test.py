import unittest

from .init_db import init_db
from .extract_sqlite_models import extract_models

DATABASE_NAME = 'database.db'


class ExtractorTestCase(unittest.TestCase):
    def setUp(self):
        init_db(DATABASE_NAME)
        extract_models(DATABASE_NAME, DATABASE_NAME.split('.')[0])

    def test_insert_user(self):
        from database import db
        id = db.user.insert(email='dsfdfsdf', password='fdgsfdgbdfg', classtype='fsvdfsdf')
        self.assertGreater(id, 0)

    def test_select_user(self):
        from database import db
        user = db(db.user.id==1).select()
        self.assertIsNotNone(user)

if __name__ == '__main__':
    unittest.main()