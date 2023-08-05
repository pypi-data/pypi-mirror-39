from abc import ABCMeta, abstractmethod


class IMessageHandler(object):
    __metaclass__ = ABCMeta

    def onMessage(self, arrivedMessage, argList):
        pass