from fastapi import FastAPI
from pydantic import BaseModel  # pip install pydantic
import uvicorn
import sqlite3

app = FastAPI(title="Book Management API", version="1.0.0")

def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
init_db()

class Book(BaseModel):
    title: str
    author: str
    year: int
    
#create book
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', 
                   (book.title, book.author, book.year))
    conn.commit()
    conn.close()
    return book

#read all books
@app.get("/books/", response_model=list[Book])
def read_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return [Book(title=row[1], author=row[2], year=row[3]) for row in books]

#read book by id
@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Book(title=row[1], author=row[2], year=row[3])
    return {"error": "Book not found"}

#update book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?',
                   (book.title, book.author, book.year, book_id))
    conn.commit()
    conn.close()
    return book

#delete book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return {"message": "Book deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)