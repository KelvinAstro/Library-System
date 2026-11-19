from flask import Flask, request, render_template
from Library_Circulation_System import Library, Shelf, Book, Patron, LibraryController

app = Flask(__name__)
library = Library()
shelf = Shelf("A1")
library.getShelves().append(shelf)
book = Book("111", "Dune", ["Herbert"], 1965, 1)
shelf.addBook(book)
p = Patron("john", "John Doe", library.nextPatronNumber())
library.addUser(p)
controller = LibraryController(library)
controller._currentUser = p  # Set the current user for testing purposes

@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    ok = False
    message = ''
    if request.method == 'POST':
        ok = controller.borrowBook(request.form['isbn'], int(request.form['copyNumber']))
        message = controller.lastMessage
    return render_template('borrow.html', ok=ok, message=message)


if __name__ == '__main__':
    app.run(debug=True)