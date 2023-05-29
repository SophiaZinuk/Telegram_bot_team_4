from telebot import types

from button.create_application_button import CreateApplicationButton
from button.applications_status_button import ApplicationStatusButton
from button.security_contacts_button import SecurityContactsButton
from button.logout_button import LogoutButton
from localization.localization import Localization
from menu.menu_type import MenuType


class Menu:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization
        super().__init__()

    def create(self, menu_type: MenuType):
        if menu_type is menu_type.MAIN:
            return self._create_main_menu()

    def _create_main_menu(self):
        markup = types.InlineKeyboardMarkup([
            [
                CreateApplicationButton(localization=self.localization),
                ApplicationStatusButton(localization=self.localization)
            ],
            [
                SecurityContactsButton(localization=self.localization),
                LogoutButton(localization=self.localization)
            ]
        ])
        return markup
