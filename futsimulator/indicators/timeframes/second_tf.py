from futsimulator.indicators.timeframes.agregator import OHLCStreamAggregator

class TimeFrame:
    
    def __init__(self, tf):
        self.tf = tf
        self.aggregator = OHLCStreamAggregator(interval_seconds=tf)
        self.total_periods = []

    def update(self, snapshot):
        record = {
            'timestamp': snapshot.datetime,
            'last': snapshot.price
        }
        tmp_periods = self.aggregator.process(record)
        self.total_periods.extend(tmp_periods)