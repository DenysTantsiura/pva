# hendlers...
from typing import Union
from ... import sort_trash
from class_note import Note
from .address_book import AddressBook
from .note_book import NoteBook


# @input_error
def handler_add_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    '''handler_add_note...": The bot creates and adds new note to the NoteBook.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            contact_dictionary (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about added note.'''

    name = user_command[1]
    text = ' '.join(user_command[2:])

    if name in note_book:
        # raise ValueError('This note already exist.')
        return ('This note already exist.')
    record = Note(name, text)
    note_book.add_record(record)
   
    return f'You added new note {name}: {text}.'

# @input_error
def handler_remove_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    '''handler_remove_note...": The bot remove note from the NoteBook.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have removed note.'''    
    
    name = user_command[1]
    if name not in note_book:
        # raise ('This note does not exist.')
        return ('This note does not exist.')
    note_book.remove_record(name)
    return (f'You have removed the note{name}.')

# @input_error
def handler_change_note(user_command: list, note_book: NoteBook, path_file: str) -> str:
    '''handler_change_note...": The bot change all note.
        Parameters:
            user_command (list): List with command, name of notes and new note's information.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about have changed note.''' 
    name = user_command[1]
    new_text = ' '.join(user_command[2:]) 
   
    if name not in note_book:
        # raise ('This note does not exist.')
        return ('This note does not exist.')
    record = note_book[name]
    record.change_note(new_text)
    return f'You have changed note.'

# @input_error
def handler_show_notes(note_book: NoteBook) -> list:
    '''handler_show_notes...": The bot shows all notes or some notes by tags.
        Parameters:
            *args (tuple): Tuple with tags or nothing.
            book (NoteBook): Dictionary with notes.
        Returns:
            list_notes (list): Return all notes.'''
   
    list_notes = ''
    for record in note_book.values():
        list_notes += f'{record}\n'
    return list_notes

# @input_error
def handler_show_note(user_command: list, note_book: NoteBook, _=None) -> str:
    '''handler_show_note...": The bot shows note wich finds by a name.
        Parameters:
            user_command (list): List with command and note's information which should adds.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            string(str): Information about showing the note.'''    
    value = user_command[1]
    try:   
        for record in note_book.values():
            if record[value]:
                return record
    except ValueError:
        return ('This note does not exist.')

# @input_error
def handler_find_notes(user_command: list, note_book: NoteBook, _=None) -> list:
    '''handler_find_notes...": The bot finds notes in the NoteBook by the tags.
        Parameters:
            user_command (list): List with command and tag.
            book (NoteBook): Dictionary with notes.
            path_file (str): Path of file record.
        Returns:
            list_notes (list): List of find notes.'''    
    
    list_notes = ''
    tags = user_command[1:]
    for tag in tags:
        for record in note_book:
            if tag in record:
                list_notes += f'{record}'
    return list_notes

# @input_error
def handler_sort_notes(__, note_book: NoteBook, _=None) -> list:
    '''handler_sort_notes...": The bot return list of note-names sorted by tags.
        Parameters:
            book (NoteBook): Dictionary with notes.
        Returns:
            list sorted note-names(list): Return list of note-names sorted by tags.'''   
    return note_book.sort_by_tags()

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
