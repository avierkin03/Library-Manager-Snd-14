from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


# Модель бази даних для автора
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Відношення "один до багатьох" з моделлю Book
    books = relationship("Book", back_populates="author")


# Модель бази даних для книги
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    pages = Column(Integer)
    # Зовнішній ключ, що посилається на таблицю authors.id
    author_id = Column(Integer, ForeignKey("authors.id"))
    # Відношення з моделлю Author
    author = relationship("Author", back_populates="books")