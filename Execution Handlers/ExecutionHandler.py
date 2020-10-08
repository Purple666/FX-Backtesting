from abc import ABCMeta, abstractmethod


class ExecutionHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        raise NotImplementedError('Should implement execute() method')
