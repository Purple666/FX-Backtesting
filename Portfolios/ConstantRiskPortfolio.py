from Portfolio import Portfolio
from Events import SignalEvent, OrderEvent
from Symbol import Symbol


class ConstantRiskPortfolio(Portfolio):
    def __init__(self, init_capital, risk):
        super(ConstantRiskPortfolio, self).__init__(init_capital)
        self.open_positions = []
        self.risk = risk

        self.value = self.init_capital
        self.free_margin = self.init_capital
        self.used_margin = 0

    def order(self, signals):
        orders = []
        for signal in signals:
            assert isinstance(signal, SignalEvent), 'Signal should be a instance of SignalEvent'
            assert isinstance(signal.symbol, Symbol), 'Signal symbol should be a instance of Symbol'
            quantity = self.risk * self.value / (10 * signal.sl)
            orders.append(OrderEvent(signal, quantity))

        return orders

    def update(self, fills):
        pass
