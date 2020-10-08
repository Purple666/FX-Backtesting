class Symbol(object):
    SYMBOLS = {'eur_usd': 4,
               'xau_usd': 1,
               'gbp_usd': 4,
               'usd_chf': 4,
               'usd_jpy': 2,
               'aud_usd': 4,
               'nzd_usd': 4,
               'usd_cad': 4,
               'gbp_aud': 4,
               'eur_gbp': 4,
               'gbp_jpy': 2,
               'gbp_cad': 2,
               'aud_jpy': 2
               }

    def __init__(self, symbol):
        assert symbol.lower() in self.SYMBOLS.keys(), 'Invalid Symbol'
        self.symbol = symbol
        self.pip_place = 10 ** (-self.SYMBOLS[symbol])

    def __repr__(self):
        return "Symbol : {} - Pip place : {}".format(self.symbol, self.pip_place)

    def __str__(self):
        return self.symbol
