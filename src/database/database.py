from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    def insertTweet(self, tweet):
        pass

    @abstractmethod
    def insertAccount(self, account):
        pass

    @abstractmethod
    def deleteTweet(self, condition):
        pass

    @abstractmethod
    def deleteAccount(self, condition):
        pass

    @abstractmethod
    def query(self, query):
        pass