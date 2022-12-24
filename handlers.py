from difflib import get_close_matches
from typing import Union

from .address_book import AddressBook

from .note_book import NoteBook
from .serialization import SaveBook


def handler_command_guesser(user_command: list, *args) -> Union[str, None]:
    """In the case of an unrecognized command, 
        the bot offers the closest similar known command.
    """
    candidates = user_command[1:]  # list of words inputed by user
    commands = []

    for word in candidates:
        commands.extend(get_close_matches(word, ALL_COMMAND))

    commands = list(dict.fromkeys(commands))

    if commands:
        return f'Command with error? Maybe something from these knowns commands?:\n{commands}\n'

    candidates = ' '.join(candidates)
    return f'...\"{candidates}\"Unknown command... Nothing even to offer for you.'


# @input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add birthday to contact."""

    name = user_command[1]
    birthday = user_command[2]
    contact_dictionary[name].add_birthday(birthday)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Birthday {birthday} for contact {name} added.' 
    
    #path_file in future


# @input_error
def handler_change_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has changed birthday for contact on new birthday."""

    name = user_command[1]
    birthday = user_command[2]
    contact_dictionary[name].change_birthday(birthday)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Birthday {birthday} for contact {name} has changed.'


# @input_error
def handler_happy_birthday(user_command: list, contact_dictionary: AddressBook, _=None) -> list:
    """Bot show birthdey for contacts."""

    return contact_dictionary.show_happy_birthday(user_command[1])


# @input_error
def handler_remove_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has removed birthday for contact. Birthday changed on 'None'."""

    name = user_command[1]
    
    if contact_dictionary.get(name, None):

        if contact_dictionary[name].birthday:
            contact_dictionary[name].remove_birthday()
            
            SaveBook().save_book(contact_dictionary, path_file)

            return f'Birthday for contact {name} has delete.'

        else:
            return f'Birthday for cottact {name} don`t added. You can add.'

    else:
        return f'Contact don`t found.'


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
    'remove_address': handler_remove_address,
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


def handler_add_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Add contact address.
       Command:             add_address
       User parameters:     contact_name
                            contact_address
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    contact_name = user_command[1]
    contact_address = ' '.join(user_command[2:])
    contact_dictionary[contact_name].add_address(contact_address)

    SaveBook().save_book(contact_dictionary, path_file)


def handler_change_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Change contact address.
       Command:             change_address
       User parameters:     contact_name
                            contact_address
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    contact_name = user_command[1]
    contact_address = ' '.join(user_command[2:])
    contact_dictionary[contact_name].change_address(contact_address)

    SaveBook().save_book(contact_dictionary, path_file)


def handler_remove_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Remove contact address.
       Command:             remove_address
       User parameters:     contact_name
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    contact_name = user_command[1]
    contact_dictionary[contact_name].remove_address()

    SaveBook().save_book(contact_dictionary, path_file)
