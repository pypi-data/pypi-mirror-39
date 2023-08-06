from yadm.aggregation import BaseAggregator


class AioAggregator(BaseAggregator):
    def __aiter__(self):
        return self._cursor
