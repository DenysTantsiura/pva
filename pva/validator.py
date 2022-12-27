from typing import Union


def input_error(handler):
    """User error handler (decorator).

        Parameters:
            handler (function): Incoming function.

        Returns:
            exception_function(function): Exception function for handler functions.

    """
    # (user_command: list, book_instance: Union[AddressBook, NoteBook], path_file: str) -> Union[str, list]:
    def exception_function(*args, **kwargs) -> Union[str, list]:
        """Exception function for handler functions."""
        try:
            result = handler(*args, **kwargs)  # (user_command, book_instance, path_file)

        except KeyError as error:
            return f'Attention! Key Error:\n{error}'

        except ValueError as error:
            return f'Attention! Value Error:\n{error}'

        except IndexError as error:
            return f'Attention! Index Error:\n{error}'
            
        except Exception as error:
            return f'Attention! Unknown Error:\n{error}'

        if result is None:
            return 'Unpredictable Error =('

        return result

    return exception_function
