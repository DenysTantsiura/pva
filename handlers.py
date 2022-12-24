# hendlers...
from typing import Union


from .address_book import AddressBook

from .serialization import SaveBook

# @input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    ...

# @input_error
def handler_add_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add email to contact."""

    name = user_command[1]
    email = user_command[2]
    contact_dictionary[name].add_email(email)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Email {email} for contact {name} added.'

# @input_error
def handler_change_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot change email for contact."""

    name = user_command[1]
    old_email = user_command[2]
    new_email = user_command[3]
    contact_dictionary[name].change_email(old_email, new_email)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Email {old_email} for contact {name} has changed on {new_email}.'

# @input_error
def handler_email(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """Bot showed email for contact."""

    name = user_command[1]
    return f'{name} have email are: {[mail.value for mail in contact_dictionary.email]}.'


# @input_error
def handler_remove_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot removed email for contact."""

    name, *emails = user_command[1], user_command[2:]

    if name in contact_dictionary:

        if len(emails) == 0:

            for email in emails:
                if contact_dictionary[name].remove_email(email) == True:

                    massage = 'Email {email} for  contact {name} has delete.'
                    SaveBook().save_book(contact_dictionary, path_file)

                else:
                    massage = 'Email {email} not find in contact {name}.'

            return massage

        else: 
            return f'Contacts{name} don`t have email.'

ALL_COMMAND_ADDRESSBOOK = {
    '?': handler_help,
    'add_address': handler_add_address,
    'add_birthday': handler_add_birthday,
    'add_email': handler_add_email,
    'add_phone': handler_add_phone,
    'add': handler_add,
    'change_address': handler_change_address,
    'change_birthday': handler_change_birthday,
    'change_email': handler_change_email,
    'change': handler_change,
    'close': handler_exit,
    'email': handler_email,
    'exit': handler_exit,
    'find': handler_find,
    'good_bye': handler_exit,
    'happy_birthday': handler_happy_birthday,
    'hello': handler_hello,
    'help': handler_help,
    'phone': handler_phone,
    'remmove_address': handler_remove_address,
    'remove_birthday': handler_remove_birthday,
    'remove_email': handler_remove_email,
    'remove_phone': handler_remove_phone,
    'remove': handler_remove,
    'show_all': handler_show_all,
    'show': handler_show,
    }

ALL_COMMAND_NOTEBOOK = {
    'add_note': handler_add_note,
    'show_notes': handler_show_notes,
    'show_note': handler_show_note,
    'remove_note': handler_remove_note,
    'change_note': handler_change_note,
    'find_notes': handler_find_notes,
    'sort_notes': handler_sort_notes,
}

ALL_COMMAND_FILESORTER = {
    'sort': handler_sort,
}

ALL_COMMAND = {'command_guesser': handler_command_guesser, }

ALL_COMMAND.update(ALL_COMMAND_ADDRESSBOOK)
ALL_COMMAND.update(ALL_COMMAND_NOTEBOOK)
ALL_COMMAND.update(ALL_COMMAND_FILESORTER)


def main_handler(user_command: list, contact_dictionary: Union[AddressBook, NoteBook], path_file: str) -> Union[str, list]:
    """Get a list of command and options, a dictionary of contacts, 
    and the path to an book file (AddressBook or NoteBook). 
    Call a certain function and return a response to a command request.

        Parameters:
            user_command (list): List of user command (list of command and options).
            contact_dictionary (AddressBook|NoteBook): Instance of AddressBook or NoteBook.
            path_file (str): Is there path and filename of address book (in str).

        Returns:
            The result of the corresponding function (list): 
            The result of the certain function is a string or a list of strings.
    """
    return ALL_COMMAND.get(user_command[0], lambda *args: None)(user_command, contact_dictionary, path_file) or 'Unknown command!'


