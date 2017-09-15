from tests.base_suite import BaseTestSuite
from tests.finance import *
from tests.finance.events.__init__ import *
from tests.helper import *
from tests.test_app import DatabaseTest, IndexTest
from tests import *


# TODO: How to write it properly?

class ApplicationTestTestSuite(BaseTestSuite):

    @staticmethod
    def get_list_of_test_classes():
        classes = FinanceTestSuite.get_list_of_test_classes() + \
                  HelperTestSuite.get_list_of_test_classes()
        classes.extend([DatabaseTest, IndexTest])
        return classes


if __name__ == "__main__":
    suite = ApplicationTestTestSuite()
    suite.create_suite()
    suite.run()
