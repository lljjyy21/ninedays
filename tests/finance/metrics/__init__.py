from tests.base_suite import BaseTestSuite


class MetricsTestSuite(BaseTestSuite):

    @staticmethod
    def get_list_of_test_classes():
        from tests.finance.metrics.stock_metric_calculator_test import StockMetricCalculatorTest
        classes = [StockMetricCalculatorTest]
        return classes


if __name__ == "__main__":
    suite = MetricsTestSuite()
    suite.create_suite()
    suite.run()
