from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from menu.start_menu import StartMenu
from unittest.mock import Mock
from telebot.types import ReplyKeyboardMarkup


localization_mock = Mock()
dynamic_localization = Mock()
localization_mock.lang = {
    'share_contacts': 'Share contacts'
}


menu_manager: MenuManager = MenuManager(
    localization=localization_mock, dynamic_localization=dynamic_localization)


def _is_start_menu_created() -> bool:
    menu = menu_manager.get_menu(MenuType.START)
    return isinstance(menu, StartMenu)


assert _is_start_menu_created() is True
