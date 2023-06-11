from typing import Optional

from menu.menu_type import MenuType
from state.menu_pagination_state import MenuPaginationState


class MenuState:

    meu_type: MenuType
    pagination: MenuPaginationState
    current_application_id: Optional[int]

    def __init__(self, menu_type: MenuType) -> None:
        self.menu_type = menu_type
        self.pagination = MenuPaginationState()
        self.current_application_id = None
