from app import app
from unittest import TestCase, main
import os


class IndexTest(TestCase):
    def test_index_pass(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    def test_index_fail(self):
        tester = app.test_client(self)
        response = tester.get('/finance', content_type='html/text')
        self.assertEqual(response.status_code, 404)


class DatabaseTest(TestCase):
    def test_database(self):
        tester = os.path.exists("finance.db")
        self.assertTrue(tester)

if __name__ == '__main__':
    main()
