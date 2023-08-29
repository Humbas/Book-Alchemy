from flask import Flask, render_template, request, redirect, url_for

from data_models import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
app.config['SECRET_KEY'] = "random string"


# accessory functions
def check_if_book_exists(book_title):
    books = Book.query.all()
    for book in books:
        if book_title == book.title:
            return True


def get_authors_length():
    return len(Author.query.all())


def check_if_bookid_exists(book_id):
    books = Book.query.all()
    for book in books:
        if book_id == book.book_id:
            return True


def check_if_authorid_exists(author_id):
    authors = Author.query.all()
    for author in authors:
        if author_id == author.author_id:
            return True


# main functions


@app.route('/')
def books():
    """show available books, when searched and by default"""
    if request.method == 'GET':
        result = request.args.get('search')  # here query will be the search inputs name
        if result:
            result = str(result)
            book_results = Book.query.filter(Book.title.like("%" + result + "%")).all()
            if len(book_results) > 0:
                message = "Available results for your book search:"
            else:
                message = f" there are no books available for {result}, please retry or go back to main list "
            return render_template("home.html", result=result, books=book_results, message=message,
                                   authors=Author.query.all(), lenght=len(book_results))
        if len(Book.query.all()) > 0:
            message = "These are the currently available books ordered by Title alphabetically"
        else:
            message = "Currently there are no books to show"
        order_by_title_book_list = db.session.query(Book). \
            order_by(Book.title.asc()). \
            all()
        return render_template('home.html', books=order_by_title_book_list, message=message, authors=Author.query.all(),
                               lenght=len(Book.query.all()))


@app.route('/add_author', methods=['GET', 'POST'])
def new_author():
    """add authors"""
    if request.method == 'POST':
        if not request.form['name'] or not request.form['birthdate'] or not request.form['date_of_death']:
            message = 'Please enter all the fields'
        else:
            new_author = Author(
                name=request.form['name'],
                birth_date=request.form['birthdate'],
                date_of_death=request.form['date_of_death']
            )
            db.session.add(new_author)
            db.session.commit()
            message = 'Author was successfully added'
            return render_template('home.html', books=Book.query.all(), message=message,  lenght=len(Book.query.all()))
    else:
        message = 'Please fill out the form to add an Author'
    return render_template('add_author.html', message=message,  lenght=len(Book.query.all()))


@app.route('/add_book', methods=['GET', 'POST'])
def new_book():
    """add books"""
    if get_authors_length() < 1:
        message = "There are no book authors to choose from"
    else:
        message = "Please fill out the form to insert a book"
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['publication_year'] or not \
                    request.form['author']:
                message = "Please enter all the fields!"
            elif not request.form['publication_year'].isdigit():
                message = "Please enter a proper year!"
            elif check_if_book_exists(request.form['title']):
                message = "Hey this book already exists!"
            else:

                new_book = Book(
                    isbn=request.form['isbn'],
                    title=request.form['title'],
                    publication_year=request.form['publication_year'],
                    author_id=request.form['author']
                )
                db.session.add(new_book)
                db.session.commit()

                message = "Book was successfully added"
                return render_template('home.html', books=Book.query.all(), message=message,  lenght=len(Book.query.all()))
    return render_template('add_book.html', authors_length=get_authors_length(), authors=Author.query.all(),
                           message=message,  lenght=len(Book.query.all()))


@app.route('/book/<int:book_id>/delete', methods=['GET'])
def delete_book(book_id):
    """deletes book"""
    if request.method == 'GET':
        if check_if_bookid_exists(book_id) is None:
            return "Book does not exist"
        db.session.query(Book).filter(Book.book_id == book_id).delete()
        db.session.commit()
        return render_template('home.html', books=Book.query.all(), authors=Author.query.all(), message="book deleted",  lenght=len(Book.query.all()))
    return render_template('home.html', books=Book.query.all(), authors=Author.query.all(),  lenght=len(Book.query.all()))


@app.route('/author/<int:author_id>/delete', methods=['GET'])
def delete_author(author_id):
    """deletes book"""
    if request.method == 'GET':
        if check_if_authorid_exists(author_id) is None:
            return "Author does not exist"
        db.session.query(Book).filter(Book.author_id == author_id).delete()
        db.session.commit()
        db.session.query(Author).filter(Author.author_id == author_id).delete()
        db.session.commit()
        return  render_template('home.html', books=Book.query.all(), authors=Author.query.all(), message="author and his books deleted",  lenght=len(Book.query.all()))
    return render_template('home.html', books=Book.query.all(), authors=Author.query.all(),  lenght=len(Book.query.all()))


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(debug=True, port=5003)
