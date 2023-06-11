class StatusAlreadyUpdatedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Status already was updated')
