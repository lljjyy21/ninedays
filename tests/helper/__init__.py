from tests.base_suite import BaseTestSuite


class HelperTestSuite(BaseTestSuite):

    @staticmethod
    def get_list_of_test_classes():
        from input_type_validator_test import InputValidatorTest
        classes = [InputValidatorTest]
        return classes


if __name__ == "__main__":
    suite = HelperTestSuite()
    suite.create_suite()
    suite.run()
