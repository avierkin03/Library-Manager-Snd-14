from pydantic import BaseModel, Field


class AuthorClient(BaseModel):
    name: str = Field(min_length=3, max_length=30)


class AuthorDB(AuthorClient):
    id: int
    books: list[BookDB] = []   # TODO BookDB 
 
    class Confiq:
        from_attributes = True
