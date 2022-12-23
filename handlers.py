from address_book import AddressBook
from classes_address_book import Record

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
        if phones[0] not in contact_dictionary[name].get_phones_str() and phones[1] not in contact_dictionary[name].get_phones_str():
            raise ValueError ("Unknown number. Check the correctness of the input")
        if phones[0] in contact_dictionary[name].get_phones_str():
            new_phone, old_phone = phones[1], phones[0]
        else: 
            new_phone, old_phone = phones[0], phones[1]
        contact_dictionary[name].remove_phone(old_phone)
        contact_dictionary[name].add_phones(new_phone)
        return f"{name}'s phone number has been changed"
    
