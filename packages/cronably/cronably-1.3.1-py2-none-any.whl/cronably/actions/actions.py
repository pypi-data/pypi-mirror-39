from abc import ABCMeta, abstractmethod


class Actions:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass

