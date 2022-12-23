from .address_book import AddressBook

#@input_error
def handler_add_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    name, *phones = user_command[0] , user_command[1:]
    if name in contact_dictionary: 
        raise ValueError ("This contact is already in the phone book. Please enter the correct name.")
    if not name or not phones:
        raise SyntaxError ("You entered an incorrect phone number or name")
    else:
        pass


#@input_error
def handler_phone(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    pass


#@input_error
def handler_remove_phone(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    pass


#@input_error
def handler_change(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    pass
