from sqlalchemy.orm import Session

from models.ocd import OcdArticleDB


def retrieve_by_id_async(session: Session, article_id: int):
    """
    Retrieves a Player by its ID from the database.

    Args:
        async_session (AsyncSession): The async version of a SQLAlchemy ORM session.
        player_id (int): The ID of the Player to retrieve.

    Returns:
        The Player matching the provided ID, or None if not found.
    """
    article = session.get(OcdArticleDB, article_id)
    return article
