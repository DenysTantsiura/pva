# pva main function for start
import sys
from typing import NoReturn


from .address_book import AddressBook
from .note_book import NoteBook
from .serialization import LoadBook, OpenBook


class PVA():
    """Main personal virtual assistant class."""
    def __init__(self) -> None:
        try:
            self.path_file = sys.argv[1]

        except IndexError:
            self.path_file = 'ABook.data'
        
        try:
            self.path_file_notes = sys.argv[2]

        except IndexError:
            self.path_file_notes = 'NoteBook.data'

        self.path_file = OpenBook(self.path_file).open_book()
        self.path_file_notes = OpenBook(self.path_file_notes).open_book()

        self.contact_dictionary, self.path_file = LoadBook(self.path_file).load_book()
        self.note_book, self.path_file_notes = LoadBook(self.path_file_notes).load_book(NoteBook)

    def start(self) -> NoReturn:
        """The main function of launching a helper console bot that recognize 
        the commands entered from the keyboard and respond according 
        to the command entered. Enter a command - get an answer.
        """
        while True:

            user_request = InputToParser().listen()

            if user_request[0] in ALL_COMMAND_ADDRESSBOOK:  # dict of commands
                bot_answer_result = OutputAnswer().show_out(user_request, self.contact_dictionary, self.path_file)
            elif user_request[0] in ALL_COMMAND_NOTEBOOK:
                bot_answer_result = OutputAnswer().show_out(user_request, self.note_book, self.path_file_notes)
            elif user_request[0] in ALL_COMMAND_FILESORTER:
                bot_answer_result = OutputAnswer().show_out(user_request, None, '')
            else:
                user_request = ['command_guesser'] + user_request
                bot_answer_result = OutputAnswer().show_out(user_request, None, '')

            if not bot_answer_result:
                break


def main() -> NoReturn:
    pva_start = PVA()
    pva_start.start()


if __name__ == '__main__':
    main()
