from services import user_service, program_service
from sqlalchemy.orm import Session
from models import new_session


def insert_default_user(session: Session):
    user_service.create_user(session, "fabian", "1801")
    user_service.create_user(session, "dustin", "2711")
    user_service.create_user(session, "iris", "2202")
    user_service.create_user(session, "charlie", "2018")

    for p in program_service.get_all_programs(session):
        p.creator_id = 1
    session.commit()


if __name__ == "__main__":
    s = new_session()
    insert_default_user(s)
    print("Done...")
