from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def answer(self, sample: dict, config: dict) -> str:
        """Return model/system answer for a sample."""
        raise NotImplementedError
