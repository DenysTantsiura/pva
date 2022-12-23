from address_book import AddressBook
from classes_address_book import Record

#@input_error
def handler_add_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """add_phone ...: The bot saves new contact and phone(s) to contact dictionary.
    User must put name of contact and one or more phone."""
    
    name, *phones = user_command[0] , user_command[1:]
    if name in contact_dictionary: 
        raise ValueError ('This contact is already in the phone book. Please enter the correct name.')
    if not name or not phones:
        raise SyntaxError ('You entered an incorrect phone number or name.')
    else:
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)
        contact_dictionary.aadd_record(record)
        return f'{name}"s phone added to the phone book.'


#@input_error
def handler_phone(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    """phone ...: The bot adds the new phone(s) to an already existing contact in contact dictionary.
    User must put name of contact with is alredy in contact dictionary and one or more phone."""
    
    name, *phones = user_command[0] , user_command[1:]
    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')    
    for phone in phones:
        contact_dictionary[name].add_phones(phone)
    return f'{name}"s phones are appdate.'
    


#@input_error
def handler_remove_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    


#@input_error
def handler_change(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    pass
