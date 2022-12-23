# command guesser
from typing import Union

ALL_COMMAND = {'aaa1', 'bbb2', 'abc3'}


def handler_command_guesser(user_command: list, *args) -> Union[str, None]:
    """In the case of an unrecognized command, 
        the bot offers the closest similar known command.
    """
    candidates = user_command[1:]
    commands = []
    for word in candidates:
        for part in ALL_COMMAND:
            if part.startswith(word):
                commands.append(part.replace('_', ' '))
    if not commands:
        for word in candidates:
            for part in ALL_COMMAND:
                if word in part:
                    commands.append(part.replace('_', ' '))
    if not commands:
        for word in candidates:
            for part in ALL_COMMAND:
                if word[:3] in part:
                    commands.append(part.replace('_', ' '))
    if commands:
        return f'Command with error? Maybe something from these knowns commands?:\n{commands}\n'

    candidates = ' '.join(candidates)
    return f'...\"{candidates}\"Unknown command... Nothing even to offer for you.'

inp = input('Enter command: ').split()
print(inp)
print(handler_command_guesser(['guess_command']+ inp))
