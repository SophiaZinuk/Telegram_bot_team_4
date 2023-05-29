from telebot import types
from button.button_callback_type import ButtonCallbackType


class ApplicationStatusButton(types.InlineKeyboardButton):

    def __init__(self, url=None, web_app=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, pay=None, login_url=None, localization=None,
                 **kwargs):
        super().__init__(localization.lang['applications_status'], url, ButtonCallbackType.APPLICATIONS_STATUS, web_app,
                         switch_inline_query,
                         switch_inline_query_current_chat,
                         callback_game, pay, login_url, **kwargs)
