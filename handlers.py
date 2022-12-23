from typing import Union

from .address_book import AddressBook


def handler_command_guesser(user_command: list, *args) -> Union[str, None]:
    """In the case of an unrecognized command, 
        the bot offers the closest similar known command.
    """
    candidates = user_command[1:]
    commands = []
    for word in candidates:
        for part in ALL_COMMAND:
            if part.startswith(word):
                commands.append(part.replace('_', ' '))
    if not commands:
        for word in candidates:
            for part in ALL_COMMAND:
                if word in part:
                    commands.append(part.replace('_', ' '))
    if not commands:
        for word in candidates:
            for part in ALL_COMMAND:
                if word[:3] in part:
                    commands.append(part.replace('_', ' '))
    if commands:
        return f'Command with error? Maybe something from these knowns commands?:\n{commands}\n'

    candidates = ' '.join(candidates)
    return f'...\"{candidates}\"Unknown command... Nothing even to offer for you.'

inp = input('Enter command: ').split()
print(inp)
print(handler_command_guesser(['guess_command']+ inp, 6, 4, 1, 5))


# @input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    ...


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
