from typing import List, Optional, Tuple

from sqlalchemy.orm import Session, Query

from db.constant.application_status import ApplicationStatus
from db.exception.status_already_updated_exception import StatusAlreadyUpdatedException
from db.model.model import Application


class ApplicationService:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_application(self, application: Application) -> None:
        self.session.add(application)
        self.session.commit()

    def update_application_status(self, app_id: int, status: str) -> Application:
        app: Application = self.session.query(Application).get(app_id)
        if app.application_status != ApplicationStatus.PENDING:
            raise StatusAlreadyUpdatedException()
        app.application_status = status
        self.session.commit()
        return app

    def find_by_user_id_with_pagination(self, user_id: int, limit: int, page: int) -> List[Application]:
        res: List[Application] = []
        offset: int = page * limit
        query = Query([Application])
        page_query = query.filter_by(created_by=user_id).limit(limit).offset(offset)
        response = self.session.execute(page_query).fetchall()
        if len(response) > 0:
            for item in response:
                res.append(item[0])
        return res

    def find_all_with_pagination(self, limit: int, page: int) -> List[Application]:
        res: List[Application] = []
        offset: int = page * limit
        query = Query([Application])
        page_query = query.limit(limit).offset(offset)
        response = self.session.execute(page_query).fetchall()
        if len(response) > 0:
            for item in response:
                res.append(item[0])
        return res

    def find_by_id(self, app_id: int) -> Optional[Application]:
        query = self.session.query(Application).filter_by(id=app_id)
        app_tuple: Optional[Tuple[Application]] = self.session.execute(query).first()
        if app_tuple is not None:
            return app_tuple[0]
        return None
