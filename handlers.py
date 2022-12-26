from difflib import get_close_matches
from typing import Union
from sort_files import sort_trash
from class_note import Note
from address_book import AddressBook
from classes_address_book import Record
from note_book import NoteBook
from serialization import SaveBook
from validator import input_error

import colorama
from colorama import Fore, Style
colorama.init()


def handler_command_guesser(user_command: list, *args) -> Union[str, None]:
    """In the case of an unrecognized command,
        the bot offers the closest similar known command.
    """
    candidates = user_command[1:]  # list of words inputed by user
    commands = []

    for word in candidates:
        commands.extend(get_close_matches(word, ALL_COMMAND))

    commands = list(dict.fromkeys(commands))
    commands = [command.replace('_', ' ') for command in commands]

    if commands:
        return f'Command with error? Maybe something from these knowns commands?:\n{commands}\n'

    candidates = ' '.join(candidates)
    return f'...\"{candidates}\" Unknown command... Nothing even to offer for you.'


@input_error
def handler_add_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_add_note: The bot creates and adds new note to the NoteBook.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            contact_dictionary (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about added note."""

    tags = []
    text_list = []
    name = user_command[1].title()
    commands = user_command[2:]

    for element in commands:
        if '#' in element:
            tags.append(element)

    for element in commands:
        if element not in tags:
            text_list.append(element)
    text = ' '.join(text_list)
    if len(text) > 0:
        if name in note_book:
            raise ValueError('This note already exist.')
        record = Note(name, text)
        note_book.add_record(record)
        print (f'You added new note - {name}: {text}.')
    if len(tags) > 0:
        if name not in note_book:
            raise ValueError('This note not exist. You should add note (<command> <name> <text> <tag>)')
        note_book[name].add_tags(tags)
    elif name in note_book:
        raise ValueError ('This note already exist.')
    elif name not in note_book:
        raise ValueError ('This note not exist.You should add note (<command> <name> <text> and / or <tag>)')
    SaveBook().save_book(note_book, path_file)

    return f'What is your next step?'


@input_error
def handler_remove_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_remove_note: The bot remove note from the NoteBook.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have removed note."""
    name = user_command[1].title()
    if name not in note_book:
        raise ValueError('This note does not exist.')
    note_book.remove_record(name)
    SaveBook().save_book(note_book, path_file)
    return (f'You have removed the note - {name}.')


@input_error
def handler_change_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_change_note: The bot change all note.
        Parameters:
            user_command (list): List with command, name of notes and new note's information.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have changed note."""

    name = user_command[1].title()
    new_text = ' '.join(user_command[2:])

    if name not in note_book:
        raise ValueError('This note does not exist.')
    record = note_book[name]
    record.change_note(new_text)
    SaveBook().save_book(note_book, path_file)
    return f'You have changed note {record}.'


@input_error
def handler_change_in_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_change_in: The bot changes part of the note.
        Parameters:
            user_command (list): List with command, name of notes and new note's information.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have changed note."""
   
    name = user_command[1].title()
    ind = user_command.index('--')
    changed_text = ' '.join(user_command[2:ind])
    new_text = ' '.join(user_command[(ind+1):]) 
    if name not in note_book:
        raise ('This note does not exist.')
    record = note_book[name]
    record.change_in(changed_text, new_text)
    SaveBook().save_book(note_book, path_file)
    return f'You have changed note {record}.'


@input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add birthday to contact."""
    name = user_command[1].title()
    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')

    birthday = user_command[2]
    if contact_dictionary[name].add_birthday(birthday):
        SaveBook().save_book(contact_dictionary, path_file)
        return f'Birthday {birthday} for contact {name} added.'

    else:
        raise ValueError ('Birthday already recorded for \"{name}\". You can change it.')


@input_error
def handler_change_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has changed birthday for contact on new birthday."""
    name = user_command[1].title()
    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.') 

    if not contact_dictionary[name].birthday:
        raise ValueError ('Birthday not specified for "{name}". You can add it.')

    birthday = user_command[2]
    contact_dictionary[name].change_birthday(birthday)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Birthday {birthday} for contact {name} has changed.'


@input_error
def handler_happy_birthday(user_command: list, contact_dictionary: AddressBook, _=None) -> list:
    """Bot show birthdey for contacts."""

    return contact_dictionary.show_happy_birthday(user_command[1])


@input_error
def handler_remove_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has removed birthday for contact. Birthday changed on 'None'."""

    name = user_command[1].title()

    if contact_dictionary.get(name, None):

        if contact_dictionary[name].birthday:
            contact_dictionary[name].remove_birthday()

            SaveBook().save_book(contact_dictionary, path_file)

            return f'Birthday for contact {name} has delete.'

        else:
            return f'Birthday for cottact {name} don`t added. You can add.'

    else:
        return f'Contact don`t found.'


@input_error
def handler_add_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add email to contact."""
    if len(user_command) == 1:
        return f'Comand "add email" add to record person email. Example:\nadd_email <username> <email1>...<new emailN>\n'

    name, emails = user_command[1].title(), user_command[2:]

    if name not in contact_dictionary:
        raise ValueError(f'Contact {name} don\'t found in records!')    

    message = ''
    for email in emails:
        result, message_result = contact_dictionary[name].add_email(email)
        message += message_result

    SaveBook().save_book(contact_dictionary, path_file)

    if not message:
        raise ValueError(f'Give me email(s) for record {name}!') 

    return message


@input_error
def handler_change_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot change email for contact."""
    if len(user_command) == 1:
        return f'Comand "change email" change person email. Example:\nchange_email <username> <email for change> <new email>\n'

    name = user_command[1].title()
    old_email = user_command[2]
    new_email = user_command[3]

    if name not in contact_dictionary:
        raise ValueError(f'Contact {name} don\'t found in records!') 

    result, message_result = contact_dictionary[name].change_email(old_email, new_email)
    if result:
        SaveBook().save_book(contact_dictionary, path_file)

    return message_result


@input_error
def handler_email(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """Bot showed email for contact."""
    if len(user_command) == 1:
        return f'Comand "email show" all known person emails. Example:\nemail <username>\n'

    name = user_command[1].title()
    if name not in contact_dictionary:
        raise ValueError(f'Contact {name} don\'t found in records!')
        
    if not contact_dictionary[name].emails:
        return f'No email in record for {name}.\n'

    return f'''{name} have email are: {' '.join([email.value for email in contact_dictionary[name].emails])}.'''


@input_error
def handler_remove_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot removed email for contact."""
    if len(user_command) == 1:
        return f'Comand "remove email" delete person email(s). Example:\nremove_email <username> <email1>...<emailN>\n'

    name, emails = user_command[1].title(), user_command[2:]

    if name in contact_dictionary:
        if len(emails) != 0:
            message = ''
            for email in emails:
                result, message_result = contact_dictionary[name].remove_email(email)
                message += message_result

            SaveBook().save_book(contact_dictionary, path_file)
            return message

        else: 
            return f'Email(s) not entered. Give me email(s) too.'
    
    return f'Unknown name: {name}.'



def handler_exit(*_) -> str:
    """The bot is terminating."""
    return 'Good bye!'


@input_error
def handler_find(user_command: list, contact_dictionary: AddressBook, _=None) -> list:
    """Find ...": The bot outputs a list of users whose name or phone number
    matches the entered one or more(with an OR setting) string without space(' ').
    """

    found_list = ['Matches:\n']

    for records in contact_dictionary.iterator(10):
        page = ''
        for record in records:
            for search_string in user_command[1:]:
                part = f'\n\n{record.name.value}'

                if record.birthday:
                    part += f'\nBirthday: {record.birthday.value.date()}' \
                        f' (Next after {record.days_to_birthday()} day(s)); '

                if record.phones:
                    part += f'\nPhone(s): '
                    for phone in record.phones:
                        part += f'{phone.value}; '

                if record.emails:
                    part += f'\nEmail(s): '
                    for email in record.emails:
                        part += f'{email.value}; '

                if record.address:
                    part += f'\nAddress: '
                    part += f'{record.address.value}.\n'

                if part.find(search_string) >= 0:
                    page += part

        found_list.append(page)

    return found_list


def handler_hello(*_) -> str:
    """The bot is welcome."""
    return 'Hello!'


def handler_help(*_) -> str:
    """The bot shows all commands."""
    return  'c - contact, p - phone, op - old phone, b - birthday, e - email, oe - old email, a - address, n - note\n'\
            '                                                                                \n'\
            'Command ContactBook\n'\
             '                                                                                \n'\
            'First command to create contact. Command "add" adds "c" and "p". Example (add c p)\n'\
            'Command "remove" delete "c". Example (remove c)\n'\
            'Command "add phone" adds "p" for "c". Example (add_phone c p)\n'\
            'Command "phone" show "p" for "c". Example (phone c)\n'\
            'Command "change phone" change "op" on "p". Example (change_phone c op p)\n'\
            'Command "remove phone" delete "p". Example (remove_phone c p)\n'\
            'Command "add email" adds "e" for "c". Example (add_email c e)\n'\
            'Command "email" show "e" for "c". Example (email c )\n'\
            'Command "change email" change "oe" on "e". Example (change_email c oe e)\n'\
            'Command "remove email" delete "e". Example (remove_email c e)\n'\
            'Command "add address" adds "a" for  "c". Example (add_address c a)\n'\
            'Command "change address" change "a". Example (change_address c a)\n'\
            'Command "remove address" delete "a". Example (remove_address c)\n'\
            'Command "add birthday" adds "b" for "c". Example (add_birthday c b)\n'\
            'Command "change birthday" change "b". Example (change_birthday c b)\n'\
            'Command "remove birthday" delete "b". Example (remove_birthday c)\n'\
            'Command "find" search information in contactbook and show match. Example (find 99) or (find aa)\n'\
            'Command "show" show all added information in "c". Example (show c)\n'\
            'Command "show all" show all contactbook. Example (show_all)\n'\
            '                                                                                \n'\
            'Command NoteBook\n'\
            '                                                                                \n'\
            'Command "add_note" add note. Example (add_note name text)\n'\
            'Command "change_note" change note. Example (change_note name text)\n'\
            'Command "remove_note" delete note. Example (remove_note name)\n'\
            'Command "find_notes" search by text. Example (find_note text)\n'\
            'Command "sort_note" sort note. Example (sort_note)\n'\
            'Command "show_note" show note. Example (show_note name)\n'\
            'Command "show_notes" show all note. Example (show_notes)\n'\
            '                                                                                \n'\
            'Command for sort file in folder\n'\
            '                                                                                \n'\
            'Command "sort". Example (sort path_folder)\n'\


@input_error
def handler_show_all(_, contact_dictionary: AddressBook, __) -> list:
    """The bot shows all contacts."""
    all_list = [Fore.CYAN + 'All contacts:\n' + Style.RESET_ALL]
    LIMIT = 10
    for records in contact_dictionary.iterator(LIMIT):
        contact_message = ''
        for record in records:
            contact_message += Fore.MAGENTA + '{:-^10}\n{}:\n{:-^10}\n'.format('', record.name.value, '') + Style.RESET_ALL

            if record.phones:
                contact_message += Fore.BLUE + 'Phone(s): ' + Style.RESET_ALL
                phones = ', '.join([phone.value for phone in record.phones])
                contact_message += Fore.GREEN + f'{phones}' + Style.RESET_ALL

            else:
                contact_message += Fore.BLUE + 'Phone(s): ' + Style.RESET_ALL
                contact_message += Fore.YELLOW + 'empty' + Style.RESET_ALL

            if record.emails:
                contact_message += Fore.BLUE + '\nEmail(s): ' + Style.RESET_ALL
                emails = ', '.join([email.value for email in record.emails])
                contact_message += Fore.GREEN + f'{emails}\n' + Style.RESET_ALL
                
            else:
                contact_message += Fore.BLUE + '\nEmail(s): ' + Style.RESET_ALL
                contact_message += Fore.YELLOW + 'empty\n' + Style.RESET_ALL

            contact_message += Fore.MAGENTA + '{:-^10}\n\n'.format('') + Style.RESET_ALL

        all_list.append(contact_message)

    return all_list


@input_error
def handler_sort(user_command: list, __=None, _=None) -> str:
    """The bot sort trash."""
    if user_command[1]:
        return sort_trash(user_command[1])
    else:
        return 'Please enter the path to the folder with you want to sort'


@input_error
def handler_add(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """add ...: The bot saves new contact and phone(s) to contact dictionary.
    User must write name of contact and one or more phone."""
    name, phones = user_command[1].title() , user_command[2:]
    if name in contact_dictionary:
        raise ValueError ('This contact is already in the phone book. Please enter the correct name.')

    if not name:  # or not phones:
        raise SyntaxError ('You entered an incorrect phone number or name.')

    else:
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)

        contact_dictionary.add_record(record)
        SaveBook().save_book(contact_dictionary, path_file)
        return f'Records \'{name}\' done.'


@input_error
def handler_add_phone(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """add_phone ...: The bot adds the new phone(s) to an already existing contact in contact dictionary.
    User must write name of contact with is alredy in contact dictionary and one or more phone."""
    name, phones = user_command[1].title() , user_command[2:]

    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')

    message_to_user = ''
    for phone in phones:
        if contact_dictionary[name].add_phone(phone):
            message_to_user += f'{name}\'s phones are appdate {phone}.\n'
            SaveBook().save_book(contact_dictionary, path_file)

        else:
            message_to_user += f'Contact {name} already have this {phone} phone number.\n'
    SaveBook().save_book(contact_dictionary, path_file)
    return message_to_user[:-1]


@input_error
def handler_phone(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """phone ...: The bot show all phones contact in contact dictionary.
    User must write name of contact with is alredy in contact dictionary."""
    name = user_command[1].title()

    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')

    if contact_dictionary[name].phones:
        phones = ' '.join(contact_dictionary[name].get_phones_list())
        return f'{name} phone(s): {phones}'


@input_error
def handler_remove_phone(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """remove phone ...: The bot remove phone(s) from contact in contact dictionary.
    User must write name and one or more phone."""
    name, phones = user_command[1].title() , user_command[2:]

    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')  

    message_to_user = ''  

    for phone in phones:
        if contact_dictionary[name].remove_phone(phone) == True:
            message_to_user += f'Phone number {phone} was delate from {name}\'s contact.\n'
        else:
            message_to_user =+ f'Phone number {phone} not specified in the {name}\'s contact.\n'
    SaveBook().save_book(contact_dictionary, path_file)
    return message_to_user[:-1]


@input_error
def handler_change(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """change ...: The bot changes phone number.
    User must write name and two phones."""
    name, phones = user_command[1].title() , user_command[2:]

    if name not in contact_dictionary:
        raise ValueError ('This contact is not in the phone book. Please enter the correct name.')

    if name in contact_dictionary:
        if len(phones) != 2:
            raise ValueError ('Input Error. Enter correct information')
        if phones[0] not in contact_dictionary[name].get_phones_list() and phones[1] not in contact_dictionary[name].get_phones_list():
            raise ValueError ('Unknown number. Check the correctness of the input')
        if phones[0] in contact_dictionary[name].get_phones_list():
            new_phone, old_phone = phones[1], phones[0]
        else:
            new_phone, old_phone = phones[0], phones[1]
        contact_dictionary[name].remove_phone(old_phone)
        contact_dictionary[name].add_phone(new_phone)
        SaveBook().save_book(contact_dictionary, path_file)

        SaveBook().save_book(contact_dictionary, path_file)
        return f"{name}'s phone number has been changed"


@input_error
def handler_remove(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """remove ...: The bot delete contact from contact dictionary.
    User must write just name."""
    name = user_command[1].title()

    if name in contact_dictionary:
        contact_dictionary.remove_record(name)
        SaveBook().save_book(contact_dictionary, path_file)
        return f'{name}\'s contact has been deleted'

    else:
        raise ValueError(f'Contact {name} is not in contact book')


@input_error
def handler_show(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """show ...: The bot show all information about contact.
    User must write just name."""
    name = user_command[1].title()
    if name not in contact_dictionary:
        raise ValueError(f'Contact {name} is not in contact book')

    message_to_user = Fore.MAGENTA + '{:-^10}\n{}:\n{:-^10}\n'.format('', name, '') + Style.RESET_ALL
    if contact_dictionary[name].phones:
        message_to_user += Fore.BLUE + 'Phone(s): ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + ' '.join(contact_dictionary[name].get_phones_list()) + Style.RESET_ALL

    else:
        message_to_user += Fore.BLUE + 'Phone(s): ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty' + Style.RESET_ALL

    if contact_dictionary[name].emails:

        message_to_user += f' Email: {contact_dictionary[name].get_emails_str()}; '
    
    if contact_dictionary[name].address:
        message_to_user += f' Address: {contact_dictionary[name].address.value}.'
    

        message_to_user += Fore.BLUE + '\nEmail(s): ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + f'{contact_dictionary[name].get_emails_str()}' + Style.RESET_ALL

    else:
        message_to_user += Fore.BLUE + '\nEmail(s): ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty' + Style.RESET_ALL

    if contact_dictionary[name].address:
        message_to_user += Fore.BLUE + '\nAddress: ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + f'{contact_dictionary[name].address.value}' + Style.RESET_ALL

    else:
        message_to_user += Fore.BLUE + '\nAddress: ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty' + Style.RESET_ALL

    if contact_dictionary[name].birthday:
        message_to_user += Fore.BLUE + '\nBirthday: ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + f'{contact_dictionary[name].birthday.value.date()} ({contact_dictionary[name].days_to_birthday()} days left until the birthday)\n' + Style.RESET_ALL

    else:
        message_to_user += Fore.BLUE + '\nBirthday: ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty\n' + Style.RESET_ALL

    message_to_user += Fore.MAGENTA + '{:-^10}'.format('') + Style.RESET_ALL


    return message_to_user


@input_error
def handler_show_notes(user_command, note_book: NoteBook, _=None) -> list:
    """handler_show_notes: The bot shows all notes or some notes by tags.
        Parameters:
            *args (tuple): Tuple with tags or nothing.
            book (NoteBook): Dictionary with notes.
        Returns:
            list_notes (list): Return all notes."""
    list_notes = ''
    tasks = user_command[1:]
    if len(tasks) == 0:
        for record in note_book.values():
            list_notes += f'{record}\n'
        return (f'{list_notes}')
    else:
        for tag in tasks:
            for record in note_book.data.values():
                for el in record.tags:
                    if tag == el:
                       list_notes += f'{tag} {record}\n'
        return f'NoteBook has - {list_notes}'


@input_error
def handler_show_note(user_command: list, note_book: NoteBook, _=None) -> str:
    """handler_show_note: The bot shows note wich finds by a name.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about showing the note.
    """
    value = user_command[1].title()
    if value not in note_book:
        raise ValueError ('This note does not exist.')
    for name, record in note_book.items():
        if value == name:
            return f'The note {record}.'


@input_error
def handler_find_notes(user_command: list, note_book: NoteBook, _=None) -> list:
    """handler_find_notes: The bot finds notes in the NoteBook by some words.
        Parameters:
            user_command (list): List with command and tag.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            list_notes (list): List of find notes."""
    list_notes = ''

    look_for_word = user_command[1:]
    if len(look_for_word) == 0:
        raise ValueError ('Try again! You should input <command> <tag> ...<tag>.')
    for word in look_for_word:
        for record in note_book.data.values():
            if word in record.text:
                list_notes += f'{record}\n'
        if len(list_notes) > 0:
            print(word)
            print(list_notes)
            list_notes = ''
    return ('What is your next step?')


@input_error
def handler_sort_notes(__, note_book: NoteBook, _=None) -> list:
    """handler_sort_notes: The bot return list of note-names sorted by tags.
        Parameters:
            book (NoteBook): Dictionary with notes.
        Returns:
            list sorted note-names(list): Return list of note-names sorted by tags."""
    list_sort_notes = note_book.sort_by_tags()
    if len(list_sort_notes) == 0:
        raise ValueError('Notes with tags are missing from Notepad. Try another way.')

    else:
        return f'Sorted notes with tags - {list_sort_notes}'


@input_error
def handler_add_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Add contact address.
       Command:             add_address
       User parameters:     contact_name
                            contact_address
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    contact_name = user_command[1].title()
    contact_address = ' '.join(user_command[2:])
    if not contact_address:
        raise ValueError('You should enter contact address with this command: \'add address <name> <address>\'.')
    if contact_name not in contact_dictionary:
        raise KeyError(f'Contact {contact_name} is not in contact book.')
    if contact_dictionary[contact_name].address is not None:
        raise ValueError(f'Contact {contact_name} already has address. If you want to change address use \'change address <name> <address>\' command.')

    contact_dictionary[contact_name].add_address(contact_address)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Address \'{contact_address}\' for contact {contact_name} successfully added.'


@input_error
def handler_change_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Change contact address.
       Command:             change_address
       User parameters:     contact_name
                            contact_address
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    contact_name = user_command[1].title()
    contact_address = ' '.join(user_command[2:])
    previous_address = contact_dictionary[contact_name].address
    if not contact_address:
        raise ValueError('You should enter contact address with this command: \'change address <name> <address>\'.')
    if contact_name not in contact_dictionary:
        raise KeyError(f'Contact {contact_name} is not in contact book.')
    if previous_address is None:
        raise ValueError(f'Contact {contact_name} has no address yet. If you want to add address use \'add address <name> <address>\' command.')

    contact_dictionary[contact_name].change_address(contact_address)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Address \'{previous_address}\' for contact {contact_name} successfully updated to address \'{contact_address}\'.'


@input_error
def handler_remove_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Remove contact address.
       Command:             remove_address
       User parameters:     contact_name
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    contact_name = user_command[1].title()
    if contact_name not in contact_dictionary:
        raise KeyError(f'Contact {contact_name} is not in contact book.')

    previous_address = contact_dictionary[contact_name].address
    if contact_dictionary[contact_name].address is None:
        raise ValueError(f'Contact {contact_name} already has no address.')

    contact_dictionary[contact_name].remove_address()

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Address \'{previous_address}\' for contact {contact_name} successfully deleted.'


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
    'change_phone': handler_change,
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
    'change_in': handler_change_in_note,
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
