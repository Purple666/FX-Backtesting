from DataLoader import DataLoader
import pickle


class PickleLoader(DataLoader):
    def __init__(self, directory):
        super(PickleLoader, self).__init__()
        self.time = None
        self.directory = directory
        self.start_time = None
        self.end_time = None
        self.resolution = None
        self.symbols = None
        self.dataset = None
        self.pip_decimal_places = None
        self.load()
        self.continue_backtest = True

    def load(self):
        file_ = open(self.directory, 'rb')
        dataset_ = pickle.load(file_)
        file_.close()

        self.time = 0
        self.start_time = dataset_['start_time']
        self.end_time = dataset_['end_time']
        self.resolution = dataset_['resolution']
        self.symbols = dataset_['symbols']
        self.dataset = dataset_['dataset']
        self.pip_decimal_places = dataset_['pip_decimal_places']

    def process(self, callback):
        for k, v in self.dataset.items():
            self.dataset[k] = callback(v)

    def get(self, n, symbol=None):
        if symbol is None:
            query = {}
            for k, v in self.dataset.items():
                query[k] = v.iloc[:self.time].iloc[-n:]
            return query
        else:
            return self.dataset[symbol].iloc[:self.time].iloc[-n:]

    def set(self):
        self.time += 1
        if self.time == min([len(v) for k, v in self.dataset.items()]):
            self.continue_backtest = False
