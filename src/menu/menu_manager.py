from localization.localization import Localization
from menu.main_menu import MainMenu
from menu.menu_type import MenuType
from menu.start_menu import StartMenu
from menu.applications_menu import ApplicationsMenu


class MenuManager:

    def __init__(self, localization: Localization) -> None:
        self.localization = localization
        self._init_menus()

    def get_menu(self, menu_type: MenuType):
        if menu_type is menu_type.START:
            return self.start_menu
        if menu_type is menu_type.MAIN:
            return self.main_menu
        if menu_type is menu_type.APPLICATIONS:
            return self.applications_menu

    def get_previous_menu(self, current_menu: MenuType):
        return self.prev_menu_mapping[current_menu]

    def _init_menus(self):
        self.start_menu = StartMenu(self.localization).create()
        self.main_menu = MainMenu(self.localization).create()
        self.applications_menu = ApplicationsMenu(self.localization).create()

        self.prev_menu_mapping = dict()
        self.prev_menu_mapping[MenuType.MAIN] = None
        self.prev_menu_mapping[MenuType.START] = None

        self.prev_menu_mapping[MenuType.APPLICATIONS] = MenuType.MAIN
