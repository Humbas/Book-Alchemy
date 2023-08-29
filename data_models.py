from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'Author'
    author_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String, nullable=False)

    def __init__(self, name, birth_date, date_of_death):
        self.name = name
        self.birth_date = birth_date
        self.date_of_death = date_of_death

    def __str__(self):
        return f'{self.name}: {self.birth_date} : {self.date_of_death}'


class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True, unique=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Author.author_id'))

    def __init__(self, isbn, title, publication_year, author_id):
        self.isbn = isbn
        self.title = title
        self.publication_year = publication_year
        self.author_id = author_id

    def __str__(self):
        return f': {self.title} : {self.publication_year} '
