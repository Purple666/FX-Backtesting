from abc import ABCMeta, abstractmethod


class Strategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute(self):
        raise NotImplementedError('Should implement compute() method')
