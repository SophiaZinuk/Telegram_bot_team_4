from typing import Optional, Tuple

from sqlalchemy.orm import Session
from db.model.user import User


class UserService:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_user_by_phone_number(self, phone_number: str) -> Optional[User]:
        query = self.session.query(User).filter_by(phone_number=phone_number)
        user_tuple: Optional[Tuple[User]] = self.session.execute(query).first()
        if user_tuple is not None:
            return user_tuple[0]
        return None
