from typing import Optional

from telebot import types
from telebot.types import KeyboardButtonPollType, WebAppInfo, KeyboardButtonRequestUser, KeyboardButtonRequestChat


class ShareContactsButton(types.KeyboardButton):

    def __init__(self, request_contact: Optional[bool] = None, request_location: Optional[bool] = None,
                 request_poll: Optional[KeyboardButtonPollType] = None, web_app: Optional[WebAppInfo] = None,
                 request_user: Optional[KeyboardButtonRequestUser] = None,
                 request_chat: Optional[KeyboardButtonRequestChat] = None, localization=None):
        super().__init__(localization.lang['share_contacts'], request_contact, request_location, request_poll, web_app,
                         request_user, request_chat)
