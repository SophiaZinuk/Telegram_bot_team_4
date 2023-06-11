from localization.dynamic_localization import DynamicLocalization
from localization.localization import Localization
from menu.admin_applications_pagination_menu import AdminApplicationsPaginationMenu
from menu.admin_single_application_menu import AdminSingleApplicationMenu
from menu.applications_menu import ApplicationsMenu
from menu.applications_pagination_menu import ApplicationsPaginationMenu
from menu.main_admin_menu import MainAdminMenu
from menu.main_menu import MainMenu
from menu.menu_type import MenuType
from menu.single_application_menu import SingleApplicationMenu
from menu.start_menu import StartMenu


class MenuManager:

    def __init__(self, localization: Localization, dynamic_localization: DynamicLocalization) -> None:
        self.localization = localization
        self.dynamic_localization = dynamic_localization
        self._init_menus()

    def get_menu_markup(self, menu_type: MenuType):
        if menu_type is menu_type.START:
            return self.start_menu.create()
        if menu_type is menu_type.MAIN:
            return self.main_menu.create()
        if menu_type is menu_type.APPLICATIONS:
            return self.applications_menu.create()
        if menu_type is menu_type.MAIN_ADMIN:
            return self.main_admin_menu.create()
        if menu_type is menu_type.SINGLE_APPLICATION_MENU:
            return self.single_application_menu.create()

    def get_menu(self, menu_type: MenuType):
        if menu_type is menu_type.START:
            return self.start_menu
        if menu_type is menu_type.MAIN:
            return self.main_menu
        if menu_type is menu_type.APPLICATIONS:
            return self.applications_menu
        if menu_type is menu_type.APPLICATIONS_PAGINATION_MENU:
            return self.applications_pagination_menu
        if menu_type is menu_type.SINGLE_APPLICATION_MENU:
            return self.single_application_menu
        if menu_type is menu_type.MAIN_ADMIN:
            return self.main_admin_menu
        if menu_type is menu_type.ADMIN_APPLICATIONS_PAGINATION_MENU:
            return self.admin_applications_pagination_menu
        if menu_type is menu_type.ADMIN_SINGLE_APPLICATION_MENU:
            return self.admin_single_application_menu

    def _init_menus(self):
        self.start_menu: StartMenu = StartMenu(self.localization)
        self.main_menu: MainMenu = MainMenu(self.localization)
        self.applications_menu: ApplicationsMenu = ApplicationsMenu(self.localization)
        self.applications_pagination_menu: ApplicationsPaginationMenu = ApplicationsPaginationMenu(
            self.localization,
            self.dynamic_localization)
        self.admin_applications_pagination_menu: AdminApplicationsPaginationMenu = AdminApplicationsPaginationMenu(
            self.localization, self.dynamic_localization)
        self.single_application_menu: SingleApplicationMenu = SingleApplicationMenu(self.localization)
        self.main_admin_menu: MainAdminMenu = MainAdminMenu(self.localization)
        self.admin_single_application_menu: AdminSingleApplicationMenu = AdminSingleApplicationMenu(self.localization)
