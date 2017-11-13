import numpy as np


class StockMetricCalculator:
    def __init__(self, data, event):
        self.data = data
        self.event = event
        self.open_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Open')
        self.close_price = StockMetricCalculator.data_frame_to_numpy_array(data, 'Close')
        self.event_sequence = event.get_events_sequence()
        self.rise_percentage = self._calculate_rise_percentage()

    def _calculate_rise_percentage(self):
        return np.true_divide((self.close_price - self.open_price), self.open_price)

    def _shifted_sequence_of_rises(self):
        rise_sequence = self._sequence_of_rises()
        shifted_rise_sequence = np.zeros(rise_sequence.shape, dtype=np.int8)

        shifted_rise_sequence[0:rise_sequence.shape[0] - 1] = rise_sequence[1: rise_sequence.shape[0]]
        shifted_rise_sequence[rise_sequence.shape[0] - 1] = 0
        return shifted_rise_sequence

    def _double_shifted_sequence_of_rises(self):
        rise_sequence = self._sequence_of_rises()
        double_shifted_rise_sequence = np.zeros(rise_sequence.shape, dtype=np.int8)

        double_shifted_rise_sequence[0:rise_sequence.shape[0] - 2] = rise_sequence[2: rise_sequence.shape[0]]
        double_shifted_rise_sequence[rise_sequence.shape[0] - 2] = 0
        double_shifted_rise_sequence[rise_sequence.shape[0] - 1] = 0
        return double_shifted_rise_sequence

    def _sequence_of_rises(self):
        rise_sequence = np.zeros(self.close_price.shape, dtype=np.int8)
        for i in range(1, self.close_price.shape[0]):
            if self.close_price[i - 1] < self.open_price[i]:
                rise_sequence[i] = 1

        return rise_sequence

    @staticmethod
    def data_frame_to_numpy_array(data, label):
        try:
            numpy_style_array = np.array(data[label].tolist())
        except Exception as e:
            print(e)
            return np.empty([0, 0])
        return numpy_style_array

    def calculate_chance_of_rise(self):
        shifted_sequence_of_rises = self._shifted_sequence_of_rises()

        event_occurrence = (self.event_sequence == 1).sum()
        next_day_rise_after_event = ((shifted_sequence_of_rises == 1) & (self.event_sequence == 1)).sum()

        if event_occurrence == 0:
            return 0.0

        return round((100.0 * next_day_rise_after_event)/event_occurrence, 2)

    def calculate_average_continuous_days(self):
        shifted_sequence_of_rises = self._shifted_sequence_of_rises()
        double_shifted_sequence_of_rises = self._double_shifted_sequence_of_rises()

        next_day_rise_after_event = ((shifted_sequence_of_rises == 1) &
                                     (self.event_sequence == 1) &
                                     (double_shifted_sequence_of_rises == 1)).sum()
        number_of_continuous_days = 0

        for i in range(shifted_sequence_of_rises.shape[0]):
            if self.event_sequence[i] & shifted_sequence_of_rises[i] == 1:
                for j in range(i + 1, shifted_sequence_of_rises.shape[0]):
                    if shifted_sequence_of_rises[j] == 1:
                        number_of_continuous_days += 1
                    else:
                        break

        if next_day_rise_after_event == 0:
            return 0.0

        return round(number_of_continuous_days/next_day_rise_after_event, 0)

    def get_metrics(self):
        metrics = dict()
        metrics["chance-of-rise"] = self.calculate_chance_of_rise()
        metrics["average-continuous-days"] = self.calculate_average_continuous_days()
        return metrics
