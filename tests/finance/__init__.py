from tests.base_suite import BaseTestSuite


class FinanceTestSuite(BaseTestSuite):

    @staticmethod
    def get_list_of_test_classes():
        from tests.finance.events import EventsTestSuite
        from tests.finance.metrics import MetricsTestSuite
        classes = EventsTestSuite.get_list_of_test_classes() + MetricsTestSuite.get_list_of_test_classes()
        return classes


if __name__ == "__main__":
    suite = FinanceTestSuite()
    suite.create_suite()
    suite.run()
