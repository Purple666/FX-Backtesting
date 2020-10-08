class Event(object):
    def __init__(self, event_type):
        self.event_type = event_type


class MarketEvent(Event):
    def __init__(self):
        super(MarketEvent, self).__init__('MARKET')


class SignalEvent(Event):
    SIGNAL_TYPES = ['BUY', 'SELL', 'BUY_STOP', 'SELL_STOP', 'BUY_LIMIT', 'SELL_LIMIT']

    def __init__(self, signal_type, symbol, datetime, sl=None, tp=None, price=None):
        super(SignalEvent, self).__init__('SIGNAL')
        if signal_type not in self.SIGNAL_TYPES:
            raise ValueError('Invalid signal type')

        self.signal_type = signal_type
        if self.signal_type in ['BUY', 'SELL']:
            self.pending = False
            assert price is None, 'Instant signals should not have price'
        else:
            self.pending = True
            assert price is not None, 'Pending signals should have price'

        if self.signal_type in ['BUY', 'BUY_STOP', 'BUY_LIMIT']:
            assert sl < tp, 'SL should be less than TP in BUY signals'
            if self.signal_type in ['BUY_STOP', 'BUY_LIMIT']:
                assert sl < price < tp, 'Execution price should be larger than SL and less than TP in BUY signals'

        if self.signal_type in ['SELL', 'SELL_STOP', 'SELL_LIMIT']:
            assert tp < sl, 'TP should be less than SL in SELL signals'
            if self.signal_type in ['SELL_STOP', 'SELL_LIMIT']:
                assert tp < price < sl, 'Execution price should be larger than TP and less than SL in SELL signals'

        self.symbol = symbol
        self.datetime = datetime
        self.sl = sl
        self.tp = tp
        self.price = price


class OrderEvent(Event):
    def __init__(self, signal, quantity):
        super(OrderEvent, self).__init__('ORDER')
        self.signal = signal
        self.quantity = quantity

    def print(self):
        if self.signal.pending:
            print("Order: Symbol={}, Type={}, Quantity={}, Stop Loss={}, Take Profit={}, Price={}" \
                  .format(self.signal.symbol, self.signal.signal_type, self.quantity, self.signal.sl, self.signal.tp,
                          self.price))
        else:
            print("Order: Symbol={}, Type={}, Quantity={}, Stop Loss={}, Take Profit={}" \
                  .format(self.signal.symbol, self.signal.signal_type, self.quantity, self.signal.sl, self.signal.tp))


class FillEvent(Event):
    def __init__(self, order, price, datetime, exchange, fill_cost, commission):
        super(FillEvent, self).__init__('FILL')
        self.order = order
        self.price = price
        self.datetime = datetime
        self.exchange = exchange
        self.fill_cost = fill_cost
        self.commission = commission
