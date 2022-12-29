from difflib import get_close_matches
from typing import Union


from .note_page import Note
from .address_book import AddressBook
from .records import Record
from .note_book import NoteBook
from .serialization import SaveBook
from .validator import input_error
from .sort_files import sort_trash

import colorama
from colorama import Fore, Style
colorama.init()


def handler_command_guesser(user_command: list, *_) -> str:
    """In the case of an unrecognized command,
        the bot offers the closest similar known command.
    """
    candidates = user_command[1:]  # list of words inputed by user
    commands = []

    for word in candidates:
        commands.extend(get_close_matches(word, ALL_COMMAND))

    commands = list(dict.fromkeys(commands))
    if commands:
        commands = [command.replace('_', ' ') for command in commands] if commands[0] != 'command_guesser' else []

    if commands:
        return f'The command has an error? Maybe one of these commands will work:\n{commands}\n'

    candidates = ' '.join(candidates)
    return f'...\"{candidates}\" Unknown command... Have nothing to offer you.'


@input_error
def handler_add_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_add_note: The bot creates and adds new note to the NoteBook.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            note_book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about added note."""
    if len(user_command) == 1:
        return f'Command \'add note\' adds note to a record. '\
               'Example:\nadd note <note title> <text>\nThe <text> may contain tags starting with a grid(#).\n'

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
    
    if text:
        if name in note_book:
            raise ValueError(f'Note \'{name}\' already exists.')

        record = Note(name, text)
        
        if tags:
            record.add_tags(tags)

        note_book.add_record(record)
        SaveBook().save_book(note_book, path_file)

        return f'Note \'{name}\' with text \'{text}\' was successfully added.'

    raise ValueError('No text entered for note!')


@input_error
def handler_remove_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_remove_note: The bot remove note from the NoteBook.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            note_book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have removed note."""
    if len(user_command) == 1:
        return f'Command \'remove note\' delete note from NoteBook. '\
               'Example:\nremove note <note title>\n'

    name = user_command[1].title()
    if name not in note_book:
        raise ValueError(f'Note {name} doesn\'t exist.')

    note_book.remove_record(name)
    SaveBook().save_book(note_book, path_file)

    return f'Note \'{name}\' was successfully removed.'


@input_error
def handler_change_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_change_note: The bot change all note.
        Parameters:
            user_command (list): List with command, name of notes and new note's information.
            note_book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have changed note."""
    if len(user_command) == 1:
        return f'Command \'change note\' change text in note. '\
               'Example:\nchange note <note title> <new text>\n'

    name = user_command[1].title()
    new_text = ' '.join(user_command[2:])

    if name not in note_book:
        raise ValueError(f'Note \'{name}\' doesn\'t exist.')

    record = note_book[name]
    record.change_note(new_text)
    SaveBook().save_book(note_book, path_file)

    return f'Note \'{name}\' was successfully updated with text \'{new_text}\'.'


@input_error
def handler_change_in_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    """handler_change_in: The bot changes part of the note.
        Parameters:
            user_command (list): List with command, name of notes and new note's information.
            note_book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have changed note."""

    name = user_command[1].title()
    ind = user_command.index('--')
    changed_text = ' '.join(user_command[2:ind])
    new_text = ' '.join(user_command[(ind+1):])
    if name not in note_book:
        raise f'Note \'{name}\' doesn\'t exist.'
    record = note_book[name]
    record.change_in(changed_text, new_text)
    SaveBook().save_book(note_book, path_file)
    return f'Note \'{name}\' was successfully updated with text \'{new_text}\'.'


@input_error
def handler_add_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add birthday to contact."""
    if len(user_command) == 1:
        return 'Command \'add birthday\' adds to record contact\'s birthday. Please enter contact name. '\
               'Example:\nadd birthday <username> <birthday(yyyy-mm-dd)>\n'
    elif len(user_command) == 2:
        return 'Command \'add birthday\' adds to record contact\'s birthday. Please enter birthday of a '\
               'contact. Example:\nadd birthday <username> <birthday(yyyy-mm-dd)>\n'

    name = user_command[1].title()

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    birthday = user_command[2]
    if contact_dictionary[name].add_birthday(birthday):
        SaveBook().save_book(contact_dictionary, path_file)
        return f'Birthday {birthday} for contact {name} was successfully added.'

    else:
        raise ValueError(f'Contact {name} already has birthday date. You can change or remove it.')


@input_error
def handler_change_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has changed birthday for contact on new birthday."""
    if len(user_command) == 1:
        return 'Command \'change birthday\' changes the contact\'s birthday. Please enter contact\'s name. '\
               'Example:\nchange birthday <username> <birthday(yyyy-mm-dd)>\n'

    name = user_command[1].title()

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    if not contact_dictionary[name].birthday:
        raise ValueError(f'Birthday is not specified for contact \'{name}\'. You can add it.')

    if len(user_command) == 2:
        return 'Command \'change birthday\' changes the contact\'s birthday. Please enter date of contact\'s birthday.'\
               ' Example:\nchange birthday <username> <birthday(yyyy-mm-dd)>\n'

    birthday = user_command[2]
    contact_dictionary[name].change_birthday(birthday)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Birthday date \'{birthday}\' for contact {name} was successfully updated.'


@input_error
def handler_happy_birthday(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """Bot show birthdey for contacts."""

    if len(user_command) == 1:
        return 'Command \'happy birthday\' shows users whose birthday is in a given range of days. Please enter range'\
               ' of days. Example:\nhappy birthday <days>\n'

    return contact_dictionary.show_happy_birthday(user_command[1])


@input_error
def handler_remove_birthday(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot has removed birthday for contact. Birthday changed on 'None'."""

    if len(user_command) == 1:
        return 'Command \'remove birthday\' remove contact\'s birthday. Please enter contact\'s name. '\
               'Example:\nremove birthday <username>\n'

    name = user_command[1].title()
    if name not in contact_dictionary:
        return f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.'

    if not contact_dictionary[name].birthday:
        return f'Birthday is not specified for contact \'{name}\'. You can add it.'

    contact_dictionary[name].remove_birthday()
    SaveBook().save_book(contact_dictionary, path_file)

    return f'Birthday date for contact \'{name}\' was successfully deleted.'


@input_error
def handler_add_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot add email to contact."""
    if len(user_command) == 1:
        return 'Command \'add email\' adds contact\'s email. Example:\nadd email <username> <email 1>...<email N>\n'

    name, emails = user_command[1].title(), user_command[2:]

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    message = ''
    for email in emails:
        result, message_result = contact_dictionary[name].add_email(email)
        message += message_result

    SaveBook().save_book(contact_dictionary, path_file)

    if not message:
        raise ValueError('You should enter email(s) with command \'add email\'. Example:\nadd email <username> '
                         '<email 1>...<email N>\n')

    return message


@input_error
def handler_change_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot change email for contact."""
    if len(user_command) == 1:
        return 'Command \'change email\' changes contact\'s email. Example:\nchange email <username> '\
               '<old email> <new email>\n'

    name = user_command[1].title()

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    if len(user_command) == 2:
        return f'Command \'change email\' changes contact\'s email. Example:\nchange email <username> '\
               '<old email> <new email>\n'

    old_email = user_command[2]
    new_email = user_command[3]

    result, message_result = contact_dictionary[name].change_email(old_email, new_email)
    if result:
        SaveBook().save_book(contact_dictionary, path_file)

    return message_result


@input_error
def handler_email(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """Bot showed email for contact."""
    if len(user_command) == 1:
        return 'Command \'email\' shows all contact\'s emails. Example:\nemail <username>\n'

    name = user_command[1].title()
    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    if not contact_dictionary[name].emails:
        return f'Contact \'{name}\' doesn\'t have emails.\n'
    emails = ' '.join([email.value for email in contact_dictionary[name].emails])
    return f'Contact \'{name}\' has next email(s): {emails}.'


@input_error
def handler_remove_email(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Bot removed email for contact."""
    if len(user_command) == 1:
        return f'Command \'remove email\' removes contact\'s email(s). Please enter contact name. '\
               'Example:\nremove email <username> <email 1>...<email N>\n'

    name, emails = user_command[1].title(), user_command[2:]

    if name not in contact_dictionary:
        return f'Unknown name: {name}.'

    if not emails:
        return f'Email(s) not entered. Give me email(s) too.'

    message = ''
    for email in emails:
        result, message_result = contact_dictionary[name].remove_email(email)
        message += message_result

    SaveBook().save_book(contact_dictionary, path_file)

    return message


def handler_exit(*_) -> str:
    """The bot is terminating."""
    return Fore.YELLOW + 'Good bye! Have some fun and take care!' + Style.RESET_ALL


@input_error
def handler_find(user_command: list, contact_dictionary: AddressBook, _=None) -> Union[list, str]:
    """Find ...": The bot outputs a list of users whose name or phone number
    matches the entered one or more(with an OR setting) string without space(' ').
    """
    if len(user_command) == 1:
        return 'Command \'find\' searches information in the contact book that fits entered query(ies). '\
               'Please enter query(ies). Example:\nfind <text 1>...<text N>\n'

    found_list = [Fore.MAGENTA + 'Search results:\n' + Style.RESET_ALL]  # Fore.MAGENTA + f'Name: ' + Style.RESET_ALL 

    flag = False

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
                    page += part[:part.find(search_string)] + Fore.LIGHTGREEN_EX + part[part.find(search_string):] + Style.RESET_ALL
                    flag = True

        found_list.append(page)

    if flag:
        return found_list

    else:
        return f'No information was found.'


def handler_hello(*_) -> str:
    """The bot is welcome."""
    help_list = Fore.LIGHTCYAN_EX + 'All available commands: \n'
    help_list += '; '.join([key.replace('_', ' ') for key in ALL_COMMAND_FILESORTER] + ['\n'])
    help_list += '; '.join([key.replace('_', ' ') for key in ALL_COMMAND_NOTEBOOK] + ['\n']) + Style.RESET_ALL
    help_list += Fore.LIGHTYELLOW_EX + '; '.join([key.replace('_', ' ') for key in ALL_COMMAND_ADDRESSBOOK] + ['\n']) + \
                 Style.RESET_ALL

    return f'{help_list}'


def handler_help(*_) -> str:
    """The bot shows all commands."""
    return Fore.YELLOW + 'Descriptions:' + Style.RESET_ALL + \
            '\nc - contact, p - phone, op - old phone, b - birthday, e - email, oe - old email, a - address, n - note\n' +\
            Fore.YELLOW + '\nCommand ContactBook:\n' + Style.RESET_ALL + \
            'First command to create contact. Command "add" adds "c" and "p". Example (add c p)\n'\
            'Command "remove" delete "c". Example (remove c)\n'\
            'Command "add phone" adds "p" for "c". Example (add phone c p)\n'\
            'Command "phone" show "p" for "c". Example (phone c)\n'\
            'Command "change phone" change "op" on "p". Example (change phone c op p)\n'\
            'Command "remove phone" delete "p". Example (remove phone c p)\n'\
            'Command "add email" adds "e" for "c". Example (add email c e)\n'\
            'Command "email" show "e" for "c". Example (email c )\n'\
            'Command "change email" change "oe" on "e". Example (change email c oe e)\n'\
            'Command "remove email" delete "e". Example (remove email c e)\n'\
            'Command "add address" adds "a" for  "c". Example (add address c a)\n'\
            'Command "change address" change "a". Example (change address c a)\n'\
            'Command "remove address" delete "a". Example (remove address c)\n'\
            'Command "add birthday" adds "b" for "c". Example (add birthday c b)\n'\
            'Command "change birthday" change "b". Example (change birthday c b)\n'\
            'Command "remove birthday" delete "b". Example (remove birthday c)\n'\
            'Command "find" search information in contactbook and show match. Example (find 99) or (find aa)\n'\
            'Command "show" show all added information in "c". Example (show c)\n'\
            'Command "show all" show all contactbook. Example (show all)' +\
            Fore.YELLOW + '\nCommand NoteBook:\n' + Style.RESET_ALL + \
            'Command "add note" add note. Example (add note name text)\n'\
            'Command "change note" change note. Example (change note name text)\n'\
            'Command "remove note" delete note. Example (remove note name)\n'\
            'Command "find notes" search by text. Example (find note text)\n'\
            'Command "sort note" sort note. Example (sort note)\n'\
            'Command "show note" show note. Example (show note name)\n'\
            'Command "show notes" show all note. Example (show notes)' +\
            Fore.YELLOW + '\nCommand for sort file in folder:\n' + Style.RESET_ALL + \
            'Command "sort". Example (sort path_folder)\n'


@input_error
def handler_show_all(_, contact_dictionary: AddressBook, __) -> list:
    """The bot shows all contacts."""
    all_list = [Fore.CYAN + 'Output of all contacts from the next page.' + Style.RESET_ALL]
    limit = 5
    for records in contact_dictionary.iterator(limit):
        contact_message = ''
        for record in records:
            contact_message += Fore.MAGENTA + '{:-^10}\nName: '.format('') + Fore.LIGHTCYAN_EX + '{}\n{:-^10}\n'.format(f'{record.name.value}', '') + \
                               Style.RESET_ALL

            if record.phones:
                contact_message += Fore.WHITE + 'Phone(s): ' + Style.RESET_ALL
                phones = ', '.join([phone.value for phone in record.phones])
                contact_message += Fore.GREEN + f'{phones}' + Style.RESET_ALL

            else:
                contact_message += Fore.WHITE + 'Phone(s): ' + Style.RESET_ALL
                contact_message += Fore.YELLOW + 'empty' + Style.RESET_ALL

            if record.emails:
                contact_message += Fore.WHITE + '\nEmail(s): ' + Style.RESET_ALL
                emails = ', '.join([email.value for email in record.emails])
                contact_message += Fore.GREEN + f'{emails}\n' + Style.RESET_ALL

            else:
                contact_message += Fore.WHITE + '\nEmail(s): ' + Style.RESET_ALL
                contact_message += Fore.YELLOW + 'empty\n' + Style.RESET_ALL

            contact_message += Fore.MAGENTA + '{:-^10}\n\n'.format('') + Style.RESET_ALL

        all_list.append(contact_message)

    return all_list


@input_error
def handler_sort(user_command: list, __=None, _=None) -> str:
    """The bot sort trash."""

    if user_command[1]:
        command_list = user_command[1:]
        command = " ".join(command_list)
        return sort_trash(command)

    else:
        return 'Please enter the path to the folder that you want to sort.'


@input_error
def handler_add(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """add ...: The bot saves new contact and phone(s) to contact dictionary.
    User must write name of contact and one or more phone."""

    if len(user_command) == 1:
        return 'Command \'add\' adds contact and phone (optional). Example:\nadd <username> <phone 1>...<phone N>\n'

    name, phones = user_command[1].title(), user_command[2:]
    if name in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' already exists. Please enter new contact name.')
    record = Record(name)
    contact_dictionary.add_record(record)
    for phone in phones:
        record.add_phone(phone)
    SaveBook().save_book(contact_dictionary, path_file)
    return f'Contact \'{name}\' was successfully added.'


@input_error
def handler_add_phone(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """add_phone ...: The bot adds the new phone(s) to an already existing contact in contact dictionary.
    User must write name of contact with is alredy in contact dictionary and one or more phone."""

    if len(user_command) == 1:
        return 'Command \'add phone\' adds contact\'s phone(s). Example:\nadd phone <username> <phone 1>...<phone N>\n'

    name, phones = user_command[1].title(), user_command[2:]

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    flag = 0
    message = ''

    for phone in phones:
        if contact_dictionary[name].add_phone(phone):
            flag += 1
            message += f'Contact \'{name}\' was successfully updated.\n'

    if flag:
        SaveBook().save_book(contact_dictionary, path_file)
        return message
    else:
        return 'If you want to add phone for contact, please use next command:\nadd phone <username> '\
               '<phone 1>...<phone N>'


@input_error
def handler_phone(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """phone ...: The bot show all phones contact in contact dictionary.
    User must write name of contact with is alredy in contact dictionary."""

    if len(user_command) == 1:
        return 'Command \'phone\' shows phone(s) for enterd contact. Example:\nphone <username>\n'

    name = user_command[1].title()

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    if contact_dictionary[name].phones:
        phones = ' '.join(contact_dictionary[name].get_phones_list())
        return f'{name} phone(s): {phones}'
    else:
        return f'Contact \'{name}\' doesn\'t have a phone number.'


@input_error
def handler_remove_phone(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """remove phone ...: The bot remove phone(s) from contact in contact dictionary.
    User must write name and one or more phone."""
    if len(user_command) == 1:
        return f'Command \'remove phone\' removes phone(s) for entered contact. Please enter contact name. '\
               'Example:\nremove phone <username> <phone 1>...<phone N>\n'

    name, phones = user_command[1].title(), user_command[2:]

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    flag = False

    for phone in phones:
        if contact_dictionary[name].remove_phone(phone):
            flag = True

    if flag:
        SaveBook().save_book(contact_dictionary, path_file)
        return f'Contact \'{name}\' was successfully updated.'
    else:
        return f'If you want to remove phone(s) for contact, please enter this command:\nremove phone <username> '\
               '<phone 1>...<phone N>'


@input_error
def handler_change(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """change ...: The bot changes phone number.
    User must write name and two phones."""
    if len(user_command) == 1:
        return 'Command \'change\' changes the phone number of the contact. Please enter contact name. '\
               'Example:\nchange <username> <old phone> <new phone>\n'

    name, phones = user_command[1].title(), user_command[2:]

    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    if name in contact_dictionary:
        if len(phones) != 2:
            raise ValueError('Command \'change\' changes the phone number of the contact. Please enter two phones. '
                             'Example:\nchange <username> <old phone> <new phone>\n')
        if phones[0] not in contact_dictionary[name].get_phones_list() and \
                phones[1] not in contact_dictionary[name].get_phones_list():
            raise ValueError('Unknown phone number. Check if the entered phone number is correct.')
        if phones[0] in contact_dictionary[name].get_phones_list():
            new_phone, old_phone = phones[1], phones[0]
        else:
            new_phone, old_phone = phones[0], phones[1]
        contact_dictionary[name].remove_phone(old_phone)
        contact_dictionary[name].add_phone(new_phone)
        SaveBook().save_book(contact_dictionary, path_file)

        SaveBook().save_book(contact_dictionary, path_file)
        return f'Phone {old_phone} for contact {name} was successfully updated with phone {new_phone}.'


@input_error
def handler_remove(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """remove ...: The bot delete contact from contact dictionary.
    User must write just name."""
    if len(user_command) == 1:
        return 'Command \'remove\' removes contact from the contact book. Example:\nremove <username>\n'

    name = user_command[1].title()

    if name in contact_dictionary:
        contact_dictionary.remove_record(name)
        SaveBook().save_book(contact_dictionary, path_file)
        return f'Contact {name} was successfully deleted.'

    else:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')


@input_error
def handler_show(user_command: list, contact_dictionary: AddressBook, _=None) -> str:
    """show ...: The bot shows all information about contact.
    User must write just name."""
    if len(user_command) == 1:
        return f'Command \'show\' shows information about contact. Example:\nshow <username>\n'

    name = user_command[1].title()
    if name not in contact_dictionary:
        raise ValueError(f'Contact \'{name}\' doesn\'t exist. Please enter name that is in the contact book.')

    message_to_user = Fore.MAGENTA + '{:-^10}\nName: '.format('') + Fore.LIGHTCYAN_EX + \
                      '{}\n{:-^10}\n'.format(f'{name}', '') + Style.RESET_ALL

    if contact_dictionary[name].phones:
        message_to_user += Fore.WHITE + 'Phone(s): ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + ' '.join(contact_dictionary[name].get_phones_list()) + Style.RESET_ALL

    else:
        message_to_user += Fore.WHITE + 'Phone(s): ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty' + Style.RESET_ALL

    if contact_dictionary[name].emails:
        message_to_user += Fore.WHITE + '\nEmail(s): ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + f'{contact_dictionary[name].get_emails_str()}' + Style.RESET_ALL

    else:
        message_to_user += Fore.WHITE + '\nEmail(s): ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty' + Style.RESET_ALL

    if contact_dictionary[name].address:
        message_to_user += Fore.WHITE + '\nAddress: ' + Style.RESET_ALL
        message_to_user += Fore.GREEN + f'{contact_dictionary[name].address.value}' + Style.RESET_ALL

    else:
        message_to_user += Fore.WHITE + '\nAddress: ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty' + Style.RESET_ALL

    if contact_dictionary[name].birthday:
        message_to_user += Fore.WHITE + '\nBirthday: ' + Style.RESET_ALL

        if contact_dictionary[name].days_to_birthday() == 365 or contact_dictionary[name].days_to_birthday() == 366:
            message_to_user += Fore.GREEN + f'{contact_dictionary[name].birthday.value.date()} (Happy Birthday!!!)\n'\
                               + Style.RESET_ALL
        else:
            message_to_user += Fore.GREEN + f'{contact_dictionary[name].birthday.value.date()} '\
                                            f'({contact_dictionary[name].days_to_birthday()} days left until '\
                                            'the birthday)\n' + Style.RESET_ALL

    else:
        message_to_user += Fore.WHITE + '\nBirthday: ' + Style.RESET_ALL
        message_to_user += Fore.YELLOW + 'empty\n' + Style.RESET_ALL

    message_to_user += Fore.MAGENTA + '{:-^10}'.format('') + Style.RESET_ALL

    return message_to_user


@input_error
def handler_show_notes(user_command, note_book: NoteBook, _=None) -> str:
    """handler_show_notes: The bot shows all notes or some notes by tags.
        Parameters:
            user_command (): (*args (tuple): Tuple with tags or nothing.)
            note_book (NoteBook): Dictionary with notes.
            _: Not important.
        Returns:
            list_notes (list): Return all notes."""
    list_notes = Fore.LIGHTCYAN_EX + ''
    tasks = user_command[1:]
    if len(tasks) == 0:
        for record in note_book.values():
            list_notes += f'{record}\n'
        if list_notes:
            return f'{list_notes}' + Style.RESET_ALL
        
        return f'No records in NoteBook.'

    for tag in tasks:
        for record in note_book.data.values():
            for el in record.tags:
                if tag == el:
                    list_notes += f'{tag} {record}\n'

    return f'NoteBook has next notes:\n{list_notes}'


@input_error
def handler_show_note(user_command: list, note_book: NoteBook, _=None) -> str:
    """handler_show_note: The bot shows note wich finds by a name.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            note_book (NoteBook): Dictionary with notes.
            _: (path_file (str): Path of file record.)
        Returns:
            string(str): Information about showing the note.
    """
    if len(user_command) == 1:
        return f'Command \'show note\' show note for user. '\
               'Example:\nshow note <note title>\n'

    value = user_command[1].title()
    if value not in note_book:
        raise ValueError(f'Note \'{value}\' doesn\'t exist.')

    return Fore.LIGHTYELLOW_EX + f'Note:\n {note_book.get(value, None)}.' + Style.RESET_ALL


@input_error
def handler_find_notes(user_command: list, note_book: NoteBook, _=None) -> str:
    """handler_find_notes: The bot finds notes in the NoteBook by some words.
        Parameters:
            user_command (list): List with command and tag.
            note_book (NoteBook): Dictionary with notes.
            _: (path_file (str): Path of file record.)
        Returns:
            list_notes (list): List of find notes."""
    if len(user_command) == 1:
        return f'Command \'find notes\' find note in notes. '\
               'Example:\nfind notes <tag 1>...<tag N>\n'
    
    list_notes = ''

    look_for_word = user_command[1:]

    for word in look_for_word:
        for record in note_book.data.values():
            if word in record.text:
                list_notes += f'{record}\n'

    if list_notes:
        return f'{word}:\n{list_notes}'

    return f'Nothing found in the notes by requests: {look_for_word}.'


@input_error
def handler_sort_notes(__, note_book: NoteBook, _=None) -> str:
    """handler_sort_notes: The bot return list of note-names sorted by tags.
        Parameters:
            __: Not inportant.
            note_book (NoteBook): Dictionary with notes.
            _: Not inportant.
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
    if len(user_command) == 1:
        return f'Command \'add_address\' adds address for contact. Example:\nadd address <username> <address>\n'

    contact_name = user_command[1].title()
    contact_address = ' '.join(user_command[2:])
    if contact_name not in contact_dictionary:
        raise KeyError(f'Contact \'{contact_name}\' doesn\'t exist. Please enter name that is in the contact book.')
    if not contact_address:
        raise ValueError('You should enter contact address with this command: \'add address <name> <address>\'.')
    if contact_dictionary[contact_name].address is not None:
        raise ValueError(f'Contact {contact_name} already has address. If you want to change address use \'change'
                         ' address <name> <address>\' command.')

    contact_dictionary[contact_name].add_address(contact_address)

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Address \'{contact_address}\' for contact {contact_name} was successfully added.'


@input_error
def handler_change_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Change contact address.
       Command:             change_address
       User parameters:     contact_name
                            contact_address
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    if len(user_command) == 1:
        return f'Command \'change address\' changes address for contact. '\
               'Example:\nchange address <username> <address>\n'

    contact_name = user_command[1].title()
    if contact_name not in contact_dictionary:
        raise KeyError(f'Contact \'{contact_name}\' doesn\'t exist. Please enter name that is in the contact book.')
    contact_address = ' '.join(user_command[2:])
    if not contact_dictionary[contact_name].address:
        raise ValueError(f'Contact {contact_name} has no address yet. If you want to add address use \'add address '
                         '<name> <address>\' command.')
    previous_address = contact_dictionary[contact_name].address
    if not contact_address:
        raise ValueError('You should enter contact address with this command: \'change address <name> <address>\'.')
    if previous_address is None:
        raise ValueError(f'Contact {contact_name} has no address yet. If you want to add address use \'add address '
                         '<name> <address>\' command.')

    if contact_dictionary[contact_name].change_address(contact_address):
        SaveBook().save_book(contact_dictionary, path_file)
        return f'Address \'{previous_address}\' for contact {contact_name} was successfully updated '\
               f'to address \'{contact_address}\'.'
    else:
        return f'Address is missing!\"{contact_address}\"'


@input_error
def handler_remove_address(user_command: list, contact_dictionary: AddressBook, path_file: str) -> str:
    """Remove contact address.
       Command:             remove_address
       User parameters:     contact_name
       Function parameters: contact_dictionary - instance of AddressBook
                            path_file - path to filename of address book
    """
    if len(user_command) == 1:
        return f'Command \'remove address\' removes address from contact. Please enter contact name. '\
               'Example:\nremove address <username>\n'
    contact_name = user_command[1].title()
    if contact_name not in contact_dictionary:
        raise KeyError(f'Contact \'{contact_name}\' doesn\'t exist. Please enter name that is in the contact book.')

    previous_address = contact_dictionary[contact_name].address
    if contact_dictionary[contact_name].address is None:
        raise ValueError(f'Contact {contact_name} already has no address.')

    contact_dictionary[contact_name].remove_address()

    SaveBook().save_book(contact_dictionary, path_file)

    return f'Address \'{previous_address}\' for contact {contact_name} was successfully deleted.'


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


def main_handler(user_command: list, contact_dictionary: Union[AddressBook, NoteBook], path_file: str) -> \
        Union[str, list]:
    """Get a list of command and options, a dictionary of contacts,
    and the path to a book file (AddressBook or NoteBook).
    Call a certain function and return a response to a command request.

        Parameters:
            user_command (list): List of user command (list of command and options).
            contact_dictionary (AddressBook|NoteBook): Instance of AddressBook or NoteBook.
            path_file (str): Is there path and filename of address book (in str).

        Returns:
            The result of the corresponding function (list):
            The result of the certain function is a string or a list of strings.
    """
    return ALL_COMMAND.get(user_command[0], lambda *args: None)(user_command, contact_dictionary, path_file) \
           or 'Unknown command!'
