from unittest import TestCase, main


class IndexTest(TestCase):
    # TODO: Add more tests to check all REST API
    def test_index_pass(self):
        from app import app
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, b'Hello, World!')

    def test_index_fail(self):
        from app import app
        tester = app.test_client(self)
        response = tester.get('/finance', content_type='html/text')
        self.assertEqual(response.status_code, 404)


class DatabaseTest(TestCase):
    # TODO: Implement later
    def test_database(self):
        #tester = os.path.exists("finance.db")
        #self.assertTrue(tester)
        pass

if __name__ == '__main__':
    main()
