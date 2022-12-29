import pickle
# from pathlib import Path
import pathlib
from typing import Union

from .address_book import AddressBook
from .note_book import NoteBook


class LoadBook:
    """Return loaded data (AddressBook or NoteBook) and path for data file."""

    def __init__(self, path_file: pathlib.Path) -> None:
        self.path_file = path_file

    def load_book(self, book=AddressBook) -> tuple[Union[AddressBook, NoteBook], pathlib.Path]:
        if not pathlib.Path.exists(self.path_file):
            new_book = book()
            # SaveBook().save_book(new_book, self.path_file)
            if SaveBook().save_book(new_book, self.path_file):
                pass
                # print('SAVED!')
            else:
                pront('NOT SAVED')
            return new_book, self.path_file

        try:
            path_file_a = pathlib.Path(self.path_file).resolve()
            with open(path_file_a, 'rb') as fh:
                data = pickle.load(fh)
        except Exception as er:
            print(f'Critical_error LOAD! path:{path_file}\nerror: {er}.')
        
        if isinstance(data, AddressBook) or isinstance(data, NoteBook):
            return data, self.path_file
        else:
            print(f'Critical_error NO LOAD!!!!{data}===================')


class OpenBook:
    """Return data file path."""

    def __init__(self, path_file: str) -> None:
        self.path_file = path_file

    def open_book(self) -> pathlib.Path:
        file_path = pathlib.Path(self.path_file)
        self.path_file = pathlib.Path(file_path.parent, file_path.name)
        return self.path_file


class SaveBook:
    """Save data in file."""

    def save_book(self, book_instance: Union[AddressBook, NoteBook], path_file: str) -> bool:
        path_file = pathlib.Path(path_file).resolve()
        with open(path_file, 'wb') as fn:
            pickle.dump(book_instance, fn)
        return True
