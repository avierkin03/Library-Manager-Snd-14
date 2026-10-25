from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Annotated
from db import models
from db.database import engine

# створює таблиці а бд, якщо вони не існують
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# pydantic-модель книги (для валідації)
class Book(BaseModel):
    title: str  
    author: Annotated[str, Field(min_length=3, max_length=30)]
    pages: Annotated[int, Field(ge=10)]


# library = {"Автор": []}
library = {}


# 1) Ендпоінт створення нової книги
@app.post("/book/")
def create_book(new_book: Book):
    if new_book.author not in library:
        library[new_book.author] = []

    for existing_book in library:
        if existing_book.title == new_book.title:
            raise HTTPException(status_code=400, detail="Така книга вже існує у цього автора")

    library[new_book.author].append(new_book)

    return {"Повідомлення": "Книгу додано", "Додана книга": new_book}


# 2) Ендпоінт отримання списку книг конкретного автора
@app.get("/books/{author}")
def get_books_by_authors(author: Annotated[str, Path(min_lenght=3, max_length=30)]):
    if author not in library:
        raise HTTPException(status_code=404, detail="Такий автор не знайдений")

    return {"Автор": author, "Список книг": library[author]}


# 3) Ендпоінт часткового оновлення книги (тільки к-ть сторінок)
@app.patch("/book/")
def update_book(updated_book: Book):
    if updated_book.author not in library:
        raise HTTPException(status_code=404, detail="Такий автор не знайдений")

    for existing_book in library:
        if existing_book.title == updated_book.title: 
            existing_book.pages = updated_book.pages
            return {"Повідомлення": "Книгу оновлено"}

    raise HTTPException(status_code=404, detail="Така книга не знайдена")


# 4) Ендпоінт видалення книги
@app.delete("/book/")
def delete_book(author: str, title: str):
    if author not in library:
        raise HTTPException(status_code=404, detail="Такий автор не знайдений")

    for existing_book in library[author]:
        if existing_book.title == title:
            library[author].remove(existing_book)
            return {"Повідомлення": "Книгу видалено"}

    raise HTTPException(status_code=404, detail="Такої книги не знайдено")