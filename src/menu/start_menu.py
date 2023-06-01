from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup
from localization.localization import Localization


class StartMenu:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization

    def create(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton(text=self.localization.lang['share_contacts'], request_contact=True))
        return markup
