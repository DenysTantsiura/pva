import pickle
from typing import Union
from pathlib import Path

from .address_book import AddressBook
from .note_book import NoteBook


class LoadBook:
    """Return loaded data (AddressBook or NoteBook) and path for data file."""

    def __init__(self, path_file: str) -> None:
        self.path_file = path_file

    def load_book(self, book) -> tuple[Union[AddressBook, NoteBook], str]:
        if not Path.exists(self.path_file):
            new_book = book()
            SaveBook().save_book(new_book, self.path_file)
            return new_book, self.path_file

        with open(self.path_file, 'rb') as fh:
            data = pickle.load(fh)
            return data, self.path_file

class OpenBook:
    """Return data file path."""

    def __init__(self, path_file: str) -> None:
        self.path_file = path_file

    def open_book(self) -> str:
        file_path = Path(self.path_file)
        self.path_file = Path(file_path.parent, file_path.name)
        return self.path_file

class SaveBook:
    """Save data in file."""

    @staticmethod
    def save_book(book_instance: Union[AddressBook, NoteBook], path_file: str) -> bool:
        with open(path_file, 'wb') as fn:
            pickle.dump(book_instance, fn)
        return True
