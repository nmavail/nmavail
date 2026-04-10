from abc import ABC, abstractmethod


class BaseChecker(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Platform name"""
        pass

    @abstractmethod
    async def check(self, name: str) -> bool | dict:
        """
        Check if a name is available.
        Returns bool: True for available, False for taken
        Returns dict: {"error": "error message"} if check fails
        """
        pass
