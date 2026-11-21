"""Unit tests for Library_Circulation_System.py

Each test checks one library rule or one requirements form the LCS spec


Run: pytest -v

"""

from datetime import date, timedelta

import pytest

from Library_Circulation_System import *

START = date(2026, 11, 2)


def add_copy(library, shelf, isbn, title, authors, year, copy):
    book = Book(isbn, title, authors, year, copy)
    shelf.addBook(book)
    book.setShelf(shelf)
    return book

@pytest.fixture
def library():
    library = Library()
    library._currentDate = START

    a1, b1 = Shelf("A1"), Shelf("B1")

    library.getShelves().extend([a1, b1])

    add_copy(library, a1, "111", "Dune", ["Herbert"], 1965, 1)
    add_copy(library, a1, "111", "Dune", ["Herbert"], 1965, 2)
    add_copy(library, a1, "111", "Dune", ["Herbert"], 1965, 3)
    add_copy(library, a1, "222", "Hiking the Appalachian Trail", ["Smith"], 1997, 1)
    add_copy(library, a1, "333", "Day Hiking in the Carolinas", ["Lee", "Smith"], 1999, 1)
    add_copy(library, b1, "444", "Hiking with Kids", ["Smith"], 2003, 1)
    add_copy(library, b1, "555", "Cooking for One", ["Jones"], 1998, 1)

    patrons = [("john", "John Doe"), ("mary", "Mary Major"), ("bob", "Bob Brown")]


    for loginID, name in patrons:
        p = Patron(loginID, name, library.nextPatronNumber())
        p.setPassword("pw")
        library.addUser(p)

    admin = Librarian("admin", "Abby Admin")
    admin.setPassword("pw")
    library.addUser(admin)

    return library


@pytest.fixture
def controller(library):
    return LibraryController(library)




