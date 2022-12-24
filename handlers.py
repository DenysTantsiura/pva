# hendlers...
from typing import Union


from .address_book import AddressBook


# @input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    ...


#@input_error
def handler_remove(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """remove ...: The bot delete contact from contact dictionary.
    User must write just name."""
    
    name = user_command[0]
    if name in contact_dictionary:
        contact_dictionary.remove_record(name)
        return f'{name}"s contact has been deleted'
    else:
        return f'Contact {name} is not in contact book'
        #raise ValueError(f'Contact {name} is not in contact book')


#@input_error
def handler_show(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    """show ...: The bot show all information about contact.
    User must write just name."""
    
    name = user_command[0]
    if name not in contact_dictionary:
        return f'Contact {name} is not in contact book'
        #raise ValueError(f'Contact {name} is not in contact book') 
    message_to_user = f'{name}: '
    if contact_dictionary[name].phones:
        message_to_user += ' '.join(contact_dictionary[name].get_phones_list())
    if contact_dictionary[name].birthday:
        message_to_user += f'; {contact_dictionary[name].days_to_birthday} days left until the birthday; '
    if contact_dictionary[name].emails:
        message_to_user += f'{contact_dictionary[name].get_emails_str}; '
    if contact_dictionary[name].address:
        message_to_user += f'address: {contact_dictionary[name].address}.'
    return message_to_user


ALL_COMMAND_ADDRESSBOOK = {
    '?': handler_help,
    'add_address': handler_add_address,
    'add_birthday': handler_add_birthday,
    'add_email': handler_add_email,
    'add_phone': handler_add_phone,
    #'add': handler_add, покищо прибираємо, залишаємо add phone
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
