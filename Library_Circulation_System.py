from __future__ import annotations

from abc import ABC
from datetime import date
from enum import Enum
from typing import List


class BookStatus(Enum):
    ON_SHELF = "ON_SHELF"
    ON_LOAN = "ON_LOAN"
    ON_HOLD = "ON_HOLD"
    ON_LOAN_AND_ON_HOLD = "ON_LOAN_AND_ON_HOLD"

class ReportType(Enum):
    BORROWED_IN_PERIOD = "BORROWED_IN_PERIOD"
    RETURNED_IN_PERIOD = "RETURNED_IN_PERIOD"
    BOOKS_ON_SHELF = "BOOKS_ON_SHELF"
    BOOKS_ON_HOLD = "BOOKS_ON_HOLD"
    PATRON_INFO = "PATRON_INFO"
    MY_BORROWED_BOOKS = "MY_BORROWED_BOOKS"
    MY_HOLDS = "MY_HOLDS"
    MY_ACCOUNT = "MY_ACCOUNT"

class User(ABC):
    def __init__(self, loginID: str, name: str):
        self.loginID = loginID
        self.name = name

        self._password = None
        self._address = None

    def getloginID(self) -> str:
        return self.loginID

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def getAddress(self) -> str | None:
        return self._address

    def setAddress(self, address: str) -> None:
        self._address = address

    def getPassword(self) -> str | None:
        return self._password

    def setPassword(self, password: str) -> None:
        self._password = password

    def verifyLogin(self, loginID: str, password: str) -> bool:
        return self.loginID == loginID and self._password == password


class Patron(User):
    def __init__(self, loginID: str, name: str, patronNumber: int):
        super().__init__(loginID, name)
        self._patronNumber = patronNumber
        self._fines: float = 0.0
        self._loans: List[LoanRecord] = []
        self._holds: List[HoldRecord] = []

    def getPatronNumber(self) -> int:
        return self._patronNumber

    def getFines(self) -> float:
        return self._fines

    def getLoans(self) -> List['LoanRecord']:
        return self._loans

    def getHolds(self) -> List['HoldRecord']:
        raise NotImplementedError("getHolds method is not implemented yet.")

    def activeLoans(self) -> List['LoanRecord']:
        return [loan for loan in self._loans if loan.isActive()]

    def canBorrow(self) -> bool:
        #TODO: Implement logic to determine if the patron can borrow more books based on active loans and fines.
        return True

    def canPlaceHold(self, isbn: str) -> bool:
        raise NotImplementedError("canPlaceHold method is not implemented yet.")

    def hasBorrowed(self, isbn: str) -> bool:
        raise NotImplementedError("hasBorrowed method is not implemented yet.")

    def hasHold(self, isbn: str) -> bool:
        raise NotImplementedError("hasHold method is not implemented yet.")

    def removeHold(self, hold: 'HoldRecord') -> None:
        self._holds.remove(hold)

    def findLoan(self, loan: 'LoanRecord') -> LoanRecord | None:
        raise NotImplementedError("findLoan method is not implemented yet.")

    def addLoan(self, loan: 'LoanRecord') -> None:
        self._loans.append(loan)

    def addHold(self, hold: 'HoldRecord') -> None:
        raise NotImplementedError("addHold method is not implemented yet.")

    def addFine(self, amount: float) -> None:
        raise NotImplementedError("addFine method is not implemented yet.")

    def payFine(self, amount: float) -> None:
        raise NotImplementedError("payFine method is not implemented yet.")


class Librarian(User):
    def __init__(self, loginID: str, name: str):
        super().__init__(loginID, name)

        self._patronAccount: Patron | None = None

    def getPatronAccount(self) -> Patron | None:
        raise NotImplementedError("getPatronAccount method is not implemented yet.")

    def setPatronAccount(self, patron: Patron) -> None:
        raise NotImplementedError("setPatronAccount method is not implemented yet.")

    def isPatron(self) -> bool:
        raise NotImplementedError("isPatron method is not implemented yet.")



class Book:
    def __init__(self, isbn: str, title: str, authors: List[str], year: int, copyNumber: int):
        self._isbn = isbn
        self._title = title
        self._authors = authors
        self._year = year
        self._copyNumber = copyNumber

        self._status: BookStatus = BookStatus.ON_SHELF
        self._loanRecord: LoanRecord | None = None
        self._holdRecords: List[HoldRecord] = []

    def getISBN(self) -> str:
        return self._isbn

    def getTitle(self) -> str:
        return self._title

    def setTitle(self, title: str) -> None:
        raise NotImplementedError("setTitle method is not implemented yet.")

    def getAuthors(self) -> List[str]:
        return self._authors

    def setAuthors(self, authors: List[str]) -> None:
        raise NotImplementedError("setAuthors method is not implemented yet.")

    def getYear(self) -> int:
        return self._year

    def setYear(self, year: int) -> None:
        raise NotImplementedError("setYear method is not implemented yet.")

    def getCopyNumber(self) -> int:
        return self._copyNumber

    def getStatus(self) -> BookStatus:
        return self._status 

    def setStatus(self, status: BookStatus) -> None:
        self._status = status

    def getShelf(self) -> str | None:
        raise NotImplementedError("getShelf method is not implemented yet.")

    def setShelf(self, shelf: str) -> None:
        raise NotImplementedError("setShelf method is not implemented yet.")

    def getCurrentLoan(self) -> LoanRecord | None:
        raise NotImplementedError("getCurrentLoan method is not implemented yet.")

    def setCurrentLoan(self, loan: 'LoanRecord') -> None:
        self._loanRecord = loan

    def getHolds(self) -> List['HoldRecord']:
        return self._holdRecords

    def setHolds(self, holds: List['HoldRecord']) -> None:
        raise NotImplementedError("setHolds method is not implemented yet.")

    def isHeldBy(self, patron: Patron) -> bool:
        #TODO: Implement logic to check if the book is held by the given patron.
        return False

    def matches(self, title: str, author: str, fromYear: int, toYear: int) -> bool:
        raise NotImplementedError("matches method is not implemented yet.")

    def conflictsWith(self, other: 'Book') -> bool:
        """Returns True if these details differ from this copy's details, indicating a conflict."""
        raise NotImplementedError("conflictsWith method is not implemented yet.")


class Shelf:

    MAX_CAPACITY = 50

    def __init__(self, shelfID: str):
        self._shelfID = shelfID
        self._books: List[Book] = []

    def getShelfID(self) -> str:
        return self._shelfID

    def getCapacity(self) -> int:
        return self.MAX_CAPACITY

    def getBooks(self) -> List[Book]:
        return self._books

    def getBookCount(self) -> int:
        raise NotImplementedError("getBookCount method is not implemented yet.")

    def isFull(self) -> bool:
        raise NotImplementedError("isFull method is not implemented yet.")

    def addBook(self, book: Book) -> None:
        self._books.append(book)

    def removeBook(self, book: Book) -> None:
        self._books.remove(book)


class LoanRecord:

    LOAN_DAYS = 14
    FINE_PER_DAY = 1.00

    def __init__(self, patron: Patron, book: Book, loanDate: date):

        self._patron: Patron = patron
        self._book: Book = book
        self._loanDate: date = loanDate
        self._dueDate: date | None = None
        self._returnDate: date | None = None
        self._renewed: bool = False

    def getPatron(self) -> Patron:
        raise NotImplementedError("getPatron method is not implemented yet.")

    def getBook(self) -> Book:
        raise NotImplementedError("getBook method is not implemented yet.")

    def getLoanDate(self) -> date:
        raise NotImplementedError("getLoanDate method is not implemented yet.")

    def getDueDate(self) -> date | None:
        return self._dueDate

    def getReturnDate(self) -> date | None:
        raise NotImplementedError("getReturnDate method is not implemented yet.")   

    def isRenewed(self) -> bool:
        raise NotImplementedError("isRenewed method is not implemented yet.")

    def isActive(self) -> bool:
        return self._returnDate is None

    def isOverdue(self) -> bool:
        raise NotImplementedError("isOverdue method is not implemented yet.")

    def calculateFine(self) -> float:
        raise NotImplementedError("calculateFine method is not implemented yet.")

    def renew(self) -> bool:
        raise NotImplementedError("renew method is not implemented yet.")

    def close(self, today: date) -> None:
        raise NotImplementedError("close method is not implemented yet.")


class HoldRecord:

    HOLD_DAYS: int = 3

    def __init__(self, patron: Patron, book: Book, holdDate: date):
        self._patron: Patron = patron
        self._book: Book = book
        self._holdDate: date = holdDate
        self._callDate: date | None = None

    def getPatron(self) -> Patron:
        raise NotImplementedError("getPatron method is not implemented yet.")

    def getBook(self) -> Book:
        raise NotImplementedError("getBook method is not implemented yet.")

    def getHoldDate(self) -> date:
        raise NotImplementedError("getHoldDate method is not implemented yet.")

    def getCallDate(self) -> date | None:
        raise NotImplementedError("getCallDate method is not implemented yet.")

    def recordCall(self, callDate: date) -> None:
        raise NotImplementedError("recordCall method is not implemented yet.")

    def isExpired(self, today: date) -> bool:
        raise NotImplementedError("isExpired method is not implemented yet.")


class Library:
    def __init__(self):
        self._currentDate: date = date.today()
        self._shelves: List[Shelf] = []
        self.users: List[User] = []
        self._lastPatronNumber: int = 0


    def getCurrentDate(self) -> date:
        return self._currentDate

    def setCurrentDate(self, currentDate: date) -> None:
        raise NotImplementedError("setCurrentDate method is not implemented yet.")

    def advanceDate(self) -> None:
        raise NotImplementedError("advanceDate method is not implemented yet.") 

    def getShelves(self) -> List[Shelf]:
        return self._shelves
    def getUsers(self) -> List[User]:
        raise NotImplementedError("getUsers method is not implemented yet.")

    def findUser(self, loginID: str) -> User | None:
        return next((user for user in self.users if user.getloginID() == loginID), None)

    def allPatrons(self) -> List[Patron]:
        raise NotImplementedError("allPatrons method is not implemented yet.")

    def addUser(self, user: User) -> None:
        self.users.append(user)

    def removeUser(self, user: User) -> None:
        raise NotImplementedError("removeUser method is not implemented yet.")

    def nextPatronNumber(self) -> int:
        self._lastPatronNumber += 1
        return self._lastPatronNumber

    def findShelf(self, shelfID: str) -> Shelf | None:
        return next((shelf for shelf in self._shelves if shelf.getShelfID() == shelfID), None)

    def findBook(self, isbn: str, copyNumber: int) -> Book | None:
        return next((book for shelf in self._shelves for book in shelf.getBooks() if book.getISBN() == isbn and book.getCopyNumber() == copyNumber), None)

    def findCopies(self, isbn: str) -> List[Book]:
        raise NotImplementedError("findCopies method is not implemented yet.")

    def allBooks(self) -> List[Book]:
        raise NotImplementedError("allBooks method is not implemented yet.")

    def nextCopyNumber(self, isbn: str) -> int:
        raise NotImplementedError("nextCopyNumber method is not implemented yet.")

    def allLoans(self) -> List[LoanRecord]:
        raise NotImplementedError("allLoans method is not implemented yet.")

    def allHolds(self) -> List[HoldRecord]:
        raise NotImplementedError("allHolds method is not implemented yet.")

class ReportGenerator:
    def __init__(self, library: Library):
        self._library = library

    def generate(self, reportType: ReportType, criteria: str, user: User) -> str:
        raise NotImplementedError("generateReport method is not implemented yet.")

    def _booksBorrowed(self, fromDate: date, toDate: date) -> str:
        raise NotImplementedError("_booksBorrowed method is not implemented yet.")

    def _booksReturned(self, fromDate: date, toDate: date) -> str:
        raise NotImplementedError("_booksReturned method is not implemented yet.")

    def _booksOnShelf(self, shelfID: str) -> str:
        raise NotImplementedError("_booksOnShelf method is not implemented yet.")

    def _booksOnHold(self, loginID: str) -> str:
        raise NotImplementedError("_booksOnHold method is not implemented yet.")
    
    def _myBorrowedBooks(self, patron: Patron) -> str:
        raise NotImplementedError("_myBorrowedBooks method is not implemented yet.")

    def _myHolds(self, patron: Patron) -> str:
        raise NotImplementedError("_myHolds method is not implemented yet.")

    def _myAccount(self, patron: Patron) -> str:
        raise NotImplementedError("_myAccount method is not implemented yet.")


class LibraryController:
    def __init__(self, library: Library):
        self._library = library
        self._reportGenerator = ReportGenerator(library)

        self._currentUser: User | None = None
        self.lastMessage: str | None = None

    def login(self, loginID: str, password: str) -> bool:
        #TODO: Implement login logic to authenticate the user based on loginID and password.
        return True

    def logout(self) -> None:
        raise NotImplementedError("logout method is not implemented yet.")

    def getCurrentUser(self) -> User | None:
        raise NotImplementedError("getCurrentUser method is not implemented yet.")

    def borrowBook(self, isbn: str, copyNumber: int) -> bool:
        #TODO: Implement logic to borrow a book based on ISBN and copy number, updating the relevant records and returning True if successful, False otherwise.
        self.lastMessage = "Book borrowed"
        return True

    def returnBook(self, isbn: str, copyNumber: int) -> bool:
        raise NotImplementedError("returnBook method is not implemented yet.")

    def placeHold(self, isbn: str) -> bool:
        raise NotImplementedError("placeHold method is not implemented yet.")

    def renewBook(self, isbn: str, copyNumber: int) -> bool:
        raise NotImplementedError("renewBook method is not implemented yet.")

    def searchBooks(self, title: str, author: str, fromYear: int, toYear: int) -> List[Book]:
        raise NotImplementedError("searchBooks method is not implemented yet.")

    def payFine(self, amount: float) -> None:
        raise NotImplementedError("payFine method is not implemented yet.")




    def nextDay(self) -> None:
        raise NotImplementedError("nextDay method is not implemented yet.")

    def addBook(self, isbn: str, title: str, authors: List[str], year: int, shelfID: str) -> bool:
        raise NotImplementedError("addBook method is not implemented yet.")

    def removeBook(self, isbn: str, copyNumber: int) -> bool:
        raise NotImplementedError("removeBook method is not implemented yet.")

    def moveBook(self, isbn: str, copyNumber: int, newShelfID: str) -> bool:
        raise NotImplementedError("moveBook method is not implemented yet.")

    def addPatron(self, loginID: str, name: str) -> bool:
        raise NotImplementedError("addPatron method is not implemented yet.")

    def updatePatron(self, loginID: str, name: str) -> bool:
        raise NotImplementedError("updatePatron method is not implemented yet.")

    def deletePatron(self, loginID: str) -> bool:
        raise NotImplementedError("deletePatron method is not implemented yet.")

    def generateReport(self, reportType: ReportType, criteria: str) -> str:
        raise NotImplementedError("generateReport method is not implemented yet.")

    def _isLibrarian(self) -> bool:
        raise NotImplementedError("_isLibrarian method is not implemented yet.")

    def _currentPatron(self) -> Patron | None:
        return self._currentUser if isinstance(self._currentUser, Patron) else None
        
class LibrarySystem:
    def __init__(self, controller: LibraryController):
        self._controller: LibraryController = controller

    def start(self) -> None:
        raise NotImplementedError("start method is not implemented yet.")

    def showMenu(self) -> None:
        raise NotImplementedError("showMenu method is not implemented yet.")

    def readInput(self) -> str:
        raise NotImplementedError("readInput method is not implemented yet.")

    def showMessage(self, message: str) -> None:
        raise NotImplementedError("showMessage method is not implemented yet.")

    def showResults(self, results: str) -> None:
        raise NotImplementedError("showResults method is not implemented yet.")

    def showReport(self, report: str) -> None:
        raise NotImplementedError("showReport method is not implemented yet.")