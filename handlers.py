# hendlers...
from typing import Union


from .address_book import AddressBook
from classes_address_book import Record


# @input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    ...


#@input_error
def handler_add_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """add_phone ...: The bot saves new contact and phone(s) to contact dictionary.
    User must write name of contact and one or more phone."""
    
    name, *phones = user_command[0] , user_command[1:]
    if name in contact_dictionary: 
        raise ValueError ('This contact is already in the phone book. Please enter the correct name.')
    if not name or not phones:
        raise SyntaxError ('You entered an incorrect phone number or name.')
    else:
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)
        if contact_dictionary.add_record(record):
            return f'{name}"s phone added to the phone book.'


#@input_error
def handler_phone(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    """phone ...: The bot adds the new phone(s) to an already existing contact in contact dictionary.
    User must write name of contact with is alredy in contact dictionary and one or more phone."""
    
    name, *phones = user_command[0] , user_command[1:]
    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')    
    message_to_user = ''
    for phone in phones:
        if contact_dictionary[name].add_phones(phone):
            message_to_user += f'{name}"s phones are appdate {phone}.\n'
        else:
            message_to_user += f'Contact {name} already have this {phone} phone number.\n '
            
    return message_to_user[:-1]


#@input_error
def handler_remove_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """remove phone ...: The bot remove phone(s) from contact in contact dictionary.
    User must write name and one or more phone"""
    
    name, *phones = user_command[0] , user_command[1:]
    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')  
    message_to_user = ''  
    for phone in phones:
        if contact_dictionary[name].remove_phone(phone) == True:
            message_to_user += f'Phone number {phone} was delate from {name}"s contact.\n'
        else:
            message_to_user =+ f'Phone number {phone} not specified in the {name}"s contact.\n'
    return message_to_user[:-1]


#@input_error
def handler_change(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """change ...: The bot changes phone number.
    User must write name ant two phones."""
    
    name, *phones = user_command[0] , user_command[1:]
    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')  
    if name in contact_dictionary:
        if len(phones) != 2:
            raise ValueError ("Input Error. Enter correct information")
        if phones[0] not in contact_dictionary[name].get_phones_list() and phones[1] not in contact_dictionary[name].get_phones_list():
            raise ValueError ("Unknown number. Check the correctness of the input")
        if phones[0] in contact_dictionary[name].get_phones_str():
            new_phone, old_phone = phones[1], phones[0]
        else: 
            new_phone, old_phone = phones[0], phones[1]
        contact_dictionary[name].remove_phone(old_phone)
        contact_dictionary[name].add_phones(new_phone)
        return f"{name}'s phone number has been changed"


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
