import abc


class Provider:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def provide(self, **kwargs):
        raise NotImplementedError('Not implemented yet!')

    @staticmethod
    def empty():
        return EmptyProvider()


class EmptyProvider(Provider):
    def provide(self, **kwargs):
        return {}
