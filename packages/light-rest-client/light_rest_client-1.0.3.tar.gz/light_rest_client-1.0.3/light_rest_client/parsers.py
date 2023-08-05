import abc

from light_rest_client.utils import from_json_to_object


class Parser:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self, body):
        raise NotImplementedError('Not implemented yet!')

    @staticmethod
    def default():
        return DefaultParser()


class DefaultParser(Parser):
    def parse(self, body):
        return body


class JSONParser(Parser):
    def parse(self, body):
        return from_json_to_object(body)
