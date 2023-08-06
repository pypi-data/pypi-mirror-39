from abc import abstractmethod

class ApplicationInterface:

    @abstractmethod
    def close_app(self):
        raise NotImplementedError()

    @abstractmethod
    def get_components(self):
        raise NotImplementedError()


