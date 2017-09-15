from tests.base_suite import BaseTestSuite


class EventsTestSuite(BaseTestSuite):

    @staticmethod
    def get_list_of_test_classes():
        from tests.finance.events.average_event_test import AverageEventTest
        from tests.finance.events.moving_average_event_test import MovingAverageEventTest
        from tests.finance.events.pass_resistance_line_test import PassResistanceLineEventTest
        from tests.finance.events.small_movement_event_test import SmallMovementEventTest
        from tests.finance.events.support_line_rebound_test import SupportLineReboundEventTest
        classes = [AverageEventTest,
                   MovingAverageEventTest,
                   PassResistanceLineEventTest,
                   SmallMovementEventTest,
                   SupportLineReboundEventTest]
        return classes


if __name__ == "__main__":
    suite = EventsTestSuite()
    suite.create_suite()
    suite.run()
