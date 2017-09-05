from unittest import TestCase, main
from helper.input_type_validator import TypeValidator


class InputValidatorTest(TestCase):

    def _build_validator_and_return_validation(self, start, end, short_ma, long_ma, range_in_days):
        validator = TypeValidator(start, end, short_ma, long_ma, range_in_days)
        return validator.validate()

    def test_data_validator_wrong_input(self):
        self.assertFalse(self._build_validator_and_return_validation(None, '2017-01-01', 1, 1, 2))
        self.assertFalse(self._build_validator_and_return_validation({}, '2017-01-01', 1, 1, 2))
        self.assertFalse(self._build_validator_and_return_validation([], '2017-01-01', 1, 1, 2))
        self.assertFalse(self._build_validator_and_return_validation((), '2017-01-01', 1, 1, 2))
        self.assertFalse(self._build_validator_and_return_validation((), '2017-01-01', 1, 1, 2))
        self.assertFalse(self._build_validator_and_return_validation('', '2017-01-01', 1, 1, 2))
        self.assertFalse(self._build_validator_and_return_validation('01-01-2017', '2017-01-01', 1, 1, 2))

        import datetime as dt
        self.assertFalse(self._build_validator_and_return_validation('2017-01-01', dt.datetime.now(), +1, 1, 100000000))

    # TODO: Need to experiment with input fields
    def test_data_validator_proper_input(self):
        self.assertTrue(self._build_validator_and_return_validation('2017-01-01', '2017-01-01', 1, 1, 2))
        self.assertTrue(self._build_validator_and_return_validation('2017-01-01', '2017-01-01', 1, 1, 100000000))
        self.assertTrue(self._build_validator_and_return_validation('2017-01-01', '2017-01-01', -1, 1, 100000000))
        self.assertTrue(self._build_validator_and_return_validation('2017-01-01', '2017-01-01', +1, 1, 100000000))

if __name__ == '__main__':
    main()
