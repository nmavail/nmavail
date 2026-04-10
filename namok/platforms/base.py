from abc import ABC, abstractmethod


class BaseChecker(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """平台名称"""
        pass

    @abstractmethod
    async def check(self, name: str) -> bool | dict:
        """
        检查名字是否可用。
        返回 bool: True 为可用, False 为已占用
        返回 dict: {"error": "错误信息"} 表示检查失败
        """
        pass
