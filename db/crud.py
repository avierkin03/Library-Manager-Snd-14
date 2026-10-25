from sqlalchemy.orm import Session
from . import models
from . import schemas

# Функція, яка читає конкретного автора (по його id)
def read_author(session: Session, author_id: int):
   return session.query(models.Author).filter(models.Author.id == author_id).first()


# Функція, яка читає всіх авторів
def read_authors(session: Session):
   return session.query(models.Author).all()


# Функція, яка створює нового автора
def create_author(session: Session, new_author: schemas.AuthorClient):
    db_author = models.Author(name = new_author.name)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author