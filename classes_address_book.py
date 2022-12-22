from typing import Union


class Field:
    ...

class Address:
    ...

class Name(Field):
    ...

class Birthday:
    ...

class Phone:
    ...

class Email:
    ...



class Record:
    """Record class of person information."""

    def __init__(self, name: str, *phones: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def __str__(self) -> str:
        return f'{self.name}, \nbirthday{self.birthday}, \nphone(s): {self.phones}, \naddress: {self.address}, \nemail(s): {self.emails}\n'

    def add_address(self, address: str) -> tuple:
        """Adds a new entry for the user's name - address."""
        if address:
            self.address = Address(address)

            return True,

        else:
            return False, f'Address is missing!\"{address}\"'

