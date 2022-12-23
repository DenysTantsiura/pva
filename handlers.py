# @input_error

def handler_add_email(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add email to contact"""

    name = user_command[1]
    return contact_dictionary[name].add_email(user_command[2])

# @input_error

def handler_change_email(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot change email for contact"""

    name = user_command[1]
    return contact_dictionary[name].change_email(user_command[2], user_command[3])

# @input_error

def handler_email(user_command: List[str], contact_dictionary: AddressBook, _=None) -> str:
    """Bot showed email for contact"""

    name = user_command[1]
    return f"{name} have email are: {[mail.value for mail in contact_dictionary.email]}"


# @input_error

def handler_remove_email(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot removed email for contact"""

    name = user_command[1]
    email = user_command[2]
    
    if name in contact_dictionary[name]:
        return contact_dictionary[name].remove_email(email)

    else:
        return f'Contact don`t found'
    
# @input_error

def handler_add_birthday(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add birthday to contact"""

    name = user_command[1]
    return contact_dictionary[name].add_birthday(user_command[2])
    
    #path_file in future


# @input_error

def handler_change_birthday(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has changed birthday for contact on new birthday"""

    name = user_command[1]
    birthday = user_command[2]
    return contact_dictionary[name].change_birthday(birthday)

# @input_error

def handler_happy_birthday(user_command: List[str], contact_dictionary: AddressBook, _=None) -> list:

    return contact_dictionary.show_happy_birthday(user_command[1])



# @input_error

def handler_remove_birthday(user_command: List[str], contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has removed birthday for contact. Birthday changed on 'None'"""

    name = user_command[1]
    
    if name in contact_dictionary[name]:
        return contact_dictionary[name].remove_birthday()

    else:
        return f'Contact don`t found'
    