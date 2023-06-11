from menu.start_menu import StartMenu
from unittest.mock import Mock


localization_mock = Mock()
localization_mock.lang = {
    'share_contacts': 'Share contacts'
}


start_menu: StartMenu = StartMenu(localization=localization_mock)


def _start_menu_markup_not_none() -> bool:
    markup = start_menu.create()
    return markup is not None


assert _start_menu_markup_not_none() is True
