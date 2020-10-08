from ExecutionHandler import ExecutionHandler
from Events import OrderEvent, FillEvent


class ExecutionHandlerSimulation(ExecutionHandler):
    def __init__(self, data_loader):
        self.instant_executions = []
        self.pending_executions = []
        self.data_loader = data_loader

    def execute(self, orders):
        for order in orders:
            assert isinstance(order, OrderEvent), 'Orders should be an instance of OrderEvent'
            if order.signal.pending:
                self.instant_executions.append({'order': order, 'clock': self.data_loader.time + 1})
            else:
                self.pending_executions.append({'order': order, 'clock': self.data_loader.time + 1})

        fills = []
        for instant_order in self.instant_executions:
            if instant_order['clock'] == self.data_loader.time:
                # Time to execute on open price
                data = self.data_loader.get(1)

                symbol = instant_order['order'].signal.symbol
                fills.append(FillEvent(instant_order['order'], data[symbol].open, self.data_loader.time, '', 0, 0))

        for pending_order in self.pending_executions:
            assert pending_order['order'].signal.pending, 'Pending executions should all be pending SignalEvents'
            if pending_order['clock'] == self.data_loader.time:
                # Check if it is possible to execute pending order
                data = self.data_loader.get(1)
                symbol = pending_order['order'].signal.symbol
                if data[symbol].low < pending_order['order'].signal.price < data[symbol].high:
                    # Can be executed in the following OHLC candle
                    fills.append(FillEvent(pending_order['order'],
                                           pending_order['order'].signal.price,
                                           self.data_loader.time, '', 0, 0))

                else:
                    # Should be checked in the future OHLC candles
                    pending_order['clock'] += 1

        return fills
