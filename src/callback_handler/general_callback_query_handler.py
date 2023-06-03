from abc import ABC, abstractmethod
from telebot import types


class GeneralCallbackQueryHandler(ABC):

    @abstractmethod
    def handle(self, callback: types.CallbackQuery):
        pass
