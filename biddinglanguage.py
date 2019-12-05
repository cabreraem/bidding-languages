import abc

class BiddingLanguage(abc.ABC):

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def to_OR(self):
        pass

    @abc.abstractmethod
    def WDP(self):
        pass