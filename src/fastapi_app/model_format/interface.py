import abc

class ModelFormatInterface(abc.ABC):
    @abc.abstractmethod
    def save_model(self, **kwargs):
        """Save the model in the specified format."""
        pass