from Strategy import Strategy
from Events import SignalEvent
from Symbol import Symbol
from ta.trend import ema


class EmaCross(Strategy):
    def __init__(self, data_loader, period, tp, sl):
        self.data_loader = data_loader
        self.period = period
        self.tp = tp  # in pips
        self.sl = sl  # in pips

        self.data_loader.process(self.pre_process())

    def pre_process(self):
        def add_ema(df):
            df['ema'] = ema(df['close'], periods=self.period, fillna=True)
            return df

        return add_ema

    def compute(self):
        if self.data_loader.time >= self.period:
            signals = []
            data = self.data_loader.get(n=1)
            for symbol, value in data.items():
                if value.close > value.ema:
                    sl_value = value.close - self.sl * 10 ** self.data_loader.pip_decimal_places[symbol]
                    tp_value = value.close + self.tp * 10 ** self.data_loader.pip_decimal_places[symbol]
                    signals.append(SignalEvent(signal_type='BUY', symbol=Symbol(symbol),
                                               datetime=value.index, sl=sl_value, tp=tp_value))
                    continue

                if value.close < value.ema:
                    sl_value = value.close + self.sl * 10 ** self.data_loader.pip_decimal_places[symbol]
                    tp_value = value.close - self.tp * 10 ** self.data_loader.pip_decimal_places[symbol]
                    signals.append(SignalEvent(signal_type='SELL', symbol=Symbol(symbol),
                                               datetime=value.index, sl=sl_value, tp=tp_value))
                    continue

            return signals
