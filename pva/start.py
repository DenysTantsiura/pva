import sys
from typing import NoReturn, Union


from .address_book import AddressBook  # .address_book import AddressBook
from .handlers import (
    main_handler,
    ALL_COMMAND,
    ALL_COMMAND_ADDRESSBOOK,
    ALL_COMMAND_NOTEBOOK,
    ALL_COMMAND_FILESORTER,
)
from .note_book import NoteBook
from .serialization import LoadBook, OpenBook


class InputToParser:

    @staticmethod
    def listen(request='How can I help you?\n'):
        """Get a user string - separate the command and parameters - 
        return it to the list, where the first element is the command, 
        the others are parameters.

            Parameters:
                request (str): String line for user request.

            Returns:
                list command of user input (list): list of commands (list of strings).
        """
        user_input = input(request)
        # Example: aDd BirthDay 2000-11-12   ->   add~birthday~2000-11-12
        command_line = user_input.strip().replace('   ', '~').replace('  ', ' ').replace(' ', '~').lower()
        # Example: ['remove~birthday', 'change~birthday' ... ]
        all_commands = sorted([el.replace('_', '~') for el in ALL_COMMAND], key=len)[::-1]

        for command in all_commands:
            command = str(command)  # Example: 'remove~birthday' ... 'add~birthday'
            if (command_line.startswith(command) and len(command_line) == len(command)) or \
                    command_line.startswith(f'{command}~'):   # Example: 'add~phone'
                # # Example: ['add_birthday'] + ['2000-11-12']
                return [command.replace('~', '_')] + [word for word in user_input[len(command):].split(' ') if word]
        # Example: ['unknown', 'command', 'abracadabra']
        return user_input.strip().split(' ')


class OutputAnswer:

    @staticmethod
    def show_out(user_request: list, book_instance: Union[AddressBook, NoteBook], new_path_file: str) -> bool:
        """Show answer for the user.
            
            Parameters:
                user_request (list): List of command with parameters (user request).
                book_instance (AddressBook|NoteBook): Instance of book.
                new_path_file (str): Path of file for book save/load.

            Returns:
                Result for new loop (bool): Answer - Do you want to continue working?.
        """
        bot_answer = main_handler(user_request, book_instance, new_path_file)

        if isinstance(bot_answer, str):
            print(bot_answer)

        elif isinstance(bot_answer, list):
            for volume in bot_answer:
                if volume:
                    print(volume)
                    input('Press Enter for next page... ')

        else:
            print('Something happened. Will you try again?')

        if 'Good bye! Have some fun and take care!' in bot_answer:
            return False 

        return True


class PVA:
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

        self.contact_dictionary, self.path_file = LoadBook(self.path_file).load_book(AddressBook)
        self.note_book, self.path_file_notes = LoadBook(self.path_file_notes).load_book(NoteBook)

        # self.parser = InputToParser()
        print('A personal virtual assistant welcomes you.\nHello!\n')

    def start(self) -> NoReturn:
        """The main function of launching a helper console bot that recognize 
        the commands entered from the keyboard and respond according 
        to the command entered. Enter a command - get an answer.
        """
        while True:

            user_request = InputToParser.listen()

            if user_request[0] in ALL_COMMAND_ADDRESSBOOK:  # dict of commands
                bot_answer_result = OutputAnswer.show_out(user_request, self.contact_dictionary, self.path_file)
            elif user_request[0] in ALL_COMMAND_NOTEBOOK:
                bot_answer_result = OutputAnswer.show_out(user_request, self.note_book, self.path_file_notes)
            elif user_request[0] in ALL_COMMAND_FILESORTER:
                bot_answer_result = OutputAnswer.show_out(user_request, None, '')
            else:
                user_request = ['command_guesser'] + user_request
                bot_answer_result = OutputAnswer.show_out(user_request, None, '')

            if not bot_answer_result:
                break


def main() -> NoReturn:
    PVA().start()


if __name__ == '__main__':
    main()
