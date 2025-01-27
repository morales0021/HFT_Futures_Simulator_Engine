from datetime import datetime, timedelta

class OHLCStreamAggregator:
    def __init__(self, interval_seconds):
        """
        Initializes the OHLC Stream Aggregator.

        Args:
            interval_minutes (int): The aggregation interval in minutes (e.g., 60 for 1-hour data).
        """
        self.interval = timedelta(seconds=interval_seconds)
        self.current_period_start = None
        self.ohlc = {'open': None, 'high': None, 'low': None, 'close': None}
        self.aggregated_data = []

    def process(self, record):
        """
        Processes a single record and updates the current OHLC aggregation.

        Args:
            record (dict): A dictionary with keys 'timestamp' (ISO string) and 'close' (float).

        Returns:
            list: A list of finalized OHLC dictionaries, if a period is completed; otherwise, an empty list.
        """
        #import pdb; pdb.set_trace()
        timestamp = record['timestamp']
        price = record['last']
        completed_periods = []
        # Start a new period if necessary
        print(timestamp, self.current_period_start, self.interval)
        if self.current_period_start is None or timestamp >= self.current_period_start + self.interval:
            # Finalize the current period if it exists

            if self.current_period_start is not None:
                completed_periods.append({
                    'timestamp': self.current_period_start.isoformat(),
                    **self.ohlc
                })
                self.aggregated_data.append(completed_periods[-1])

            # Start a new period
            self.current_period_start = timestamp.replace(microsecond=0)
            self.ohlc = {'open': price, 'high': price, 'low': price, 'close': price}
        else:
            # Update OHLC for the current period
            self.ohlc['high'] = max(self.ohlc['high'], price)
            self.ohlc['low'] = min(self.ohlc['low'], price)
            self.ohlc['close'] = price

        return completed_periods
