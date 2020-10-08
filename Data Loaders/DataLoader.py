from abc import ABCMeta, abstractmethod


class DataLoader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self):
        raise NotImplementedError('Should implement get() method')

    def set(self):
        raise NotImplementedError('Should implement set() method')
