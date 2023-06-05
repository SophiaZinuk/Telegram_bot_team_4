from sqlalchemy.orm import Session

from db.model.model import Application


class ApplicationService:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_application(self, application: Application) -> None:
        self.session.add(application)
        self.session.commit()
