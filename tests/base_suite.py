import unittest


class BaseTestSuite(object):
    def __init__(self):
        self.suite = unittest.TestSuite()

    @staticmethod
    def get_list_of_test_classes():
        classes = []
        return classes

    def create_suite(self):
        classes = self.get_list_of_test_classes()
        for test_class in classes:
            self.suite.addTest(unittest.makeSuite(test_class))
        return self.suite

    def run(self):
        runner = unittest.TextTestRunner()
        runner.run(self.suite)
