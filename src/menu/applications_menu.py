from telebot import types

from callback_handler.callback_type import CallbackType
from localization.localization import Localization


class ApplicationsMenu:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization

    def create(self):
        markup = types.InlineKeyboardMarkup([
            [
                types.InlineKeyboardButton(text=self.localization.lang['car'],
                                           callback_data=CallbackType.TAXI),
                types.InlineKeyboardButton(text=self.localization.lang['guests'],
                                           callback_data=CallbackType.GUESTS)
            ],
            # [
            #     types.InlineKeyboardButton(text=self.localization.lang['guests'],
            #                                callback_data=CallbackType.GUESTS),
            #     types.InlineKeyboardButton(text=self.localization.lang['parking_problems'],
            #                                callback_data=CallbackType.PARKING_PROBLEMS),
            # ],
            [
                types.InlineKeyboardButton(text=self.localization.lang['parking_problems'],
                                           callback_data=CallbackType.PARKING_PROBLEMS),
                types.InlineKeyboardButton(text=self.localization.lang['back'],
                                           callback_data=CallbackType.APPLICATIONS_BACK),
            ]
        ])

        return markup
