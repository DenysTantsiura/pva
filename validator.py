# Validator

from typing import Union

from .address_book import AddressBook
from .note_book import NoteBook


def input_error(handler):
    """User error handler (decorator).

        Parameters:
            handler (function): Incoming function.

        Returns:
            exception_function(function): Exception function for handler functions.

    """
    def exception_function(user_command: list, book_instance: Union[AddressBook, NoteBook],
                           path_file: str) -> Union[str, list]:
        """Exception function for handler functions."""
        try:
            result = handler(user_command, book_instance, path_file)

        except KeyError as error:
            return f'Attention! Error:\n{error}\n'

        except ValueError as error:
            return f'Attention! Error:\n{error}\n'

        except IndexError as error:
            return f'Attention! Error:\n{error}\n'
            
        except Exception as error:
            return f'Attention! Error:\n{error}\n'

        if result is None:
            return 'Unpredictable Error =('

        return result

    return exception_function
    