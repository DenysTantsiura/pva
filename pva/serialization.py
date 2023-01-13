from abc import ABC, abstractmethod
import pickle
import pathlib
from typing import Union

from address_book import AddressBook
from note_book import NoteBook


class CheckingFile(ABC):

    @abstractmethod
    def open_book(self, *args, **kwargs):
        ...

 
class FileSaver(ABC):

    @abstractmethod
    def save_book(self, *args, **kwargs):
        ...       


class LoadFromFile(ABC):

    @abstractmethod
    def load_book(self, *args, **kwargs):
        ...


class LoadBook(LoadFromFile):
    """Return loaded data (AddressBook or NoteBook) and path for data file."""

    def __init__(self, path_file: pathlib.Path) -> None:
        self.path_file = path_file

    def load_book(self, book=AddressBook) -> tuple[Union[AddressBook, NoteBook], pathlib.Path]:
        """Create empty book (AddressBook|NoteBook) if no file on path_file.
        Or, try to load book database (read) from file. 
        Return loaded book (AddressBook|NoteBook) and path for address book file.

            Parameters:
                book (AddressBook|NoteBook): Is class of book type.

            Returns:
                book_instance (AddressBook|NoteBook): Loaded from file or new empty class.
                self.path_file (pathlib.Path): The file name to save the book in the following steps.
                    Unoccupied name of file, if an exception occurred.
        """
        self.path_file = pathlib.Path(self.path_file)
        if not pathlib.Path.exists(self.path_file):
            new_book = book()
            # SaveBook().save_book(new_book, self.path_file)
            if not SaveBook().save_book(new_book, self.path_file):
                print('THE BOOK IS NOT SAVED')  # raise ...Error...!!!!!

            return new_book, self.path_file

        try:
            path_file_a = pathlib.Path(self.path_file).resolve()
            with open(path_file_a, 'rb') as fh:
                data_book = pickle.load(fh)

        except Exception as error_:
            print(f'No access to File({path_file_a}) or file is corrupted. Error: \n{repr(error_)}')
        
        if isinstance(data_book, AddressBook) or isinstance(data_book, NoteBook):
            return data_book, self.path_file

        else:
            print(f'Fatal error: Unable to load: {data_book}')


class OpenBook(CheckingFile):
    """Return data file path."""

    def __init__(self, path_file: str) -> None:
        self.path_file = path_file

    def open_book(self) -> pathlib.Path:
        """Checks if the database file exists and checks if the filename is free if not.
        If exist folder with path_file file name, then return new free file name. 
        Return unoccupied name of file (string).

            Parameters:
                self.path_file (str): Is proposed name of file.

            Returns:
                path_file (pathlib.Path): Unoccupied name(with path) of file.
        """
        file_path = pathlib.Path(self.path_file)
        while pathlib.Path.is_dir(file_path):
            self.path_file = pathlib.Path(file_path.parent, 'new_one_' + file_path.name)

        return self.path_file


class SaveBook(FileSaver):
    """Save data in file."""
    
    def save_book(self, book_instance: Union[AddressBook, NoteBook], path_file: str) -> bool:
        """Save a class AddressBook|NoteBook to a file (path_file).

            Parameters:
                book_instance (AddressBook|NoteBook): Instance of AddressBook|NoteBook.
                path_file (str): Is there path and filename of book.

            Returns:
                File save success marker (bool).
        """
        path_file = pathlib.Path(path_file).resolve()
        try:
            with open(path_file, 'wb') as fn:
                pickle.dump(book_instance, fn)
        
        except Exception as error_:
            print(f'No access to File({path_file_a}) or others fatal error: \n{repr(error_)}') 

        return True
