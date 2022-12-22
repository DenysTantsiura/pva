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

    def add_birthday(self, birthday: str) -> tuple:
        """Adds a new entry for the user's birthday to the address book."""
        if not self.birthday:
            self.birthday = Birthday(birthday)

            return True,

        else:
            return False, f'Birthday already recorded for \"{self.name.value}\"You can change it.'

    def add_phone(self, phone_new: str) -> bool:
        """Adds a new entry for the user's phone to the address book."""
        phone_new1 = Phone(phone_new)

        for phone in self.phones:
            if phone_new1 == phone.value:
                print(f'\"{phone_new1}\" already recorded for \"{self.name.value}\"')

                return False

        self.phones.append(phone_new1)

        return True
    
    def add_email(self, email_new: str) -> bool:
        """Adds a new entry for the user's email to the address book."""
        email_new1 = Email(email_new)

        for email in self.emails:
            if email_new1 == email.value:
                print(f'\"{email_new1}\" already recorded for \"{self.name.value}\"')

                return False

        self.emails.append(email_new1)

        return True

    def change_address(self, new_address: str) -> tuple:
        """Modify an existing user's address entry in the address book."""
        if new_address:
            self.address = Address(new_address)
            return True,

        else:
            return False, f'Address is missing!\"{new_address}\"'

    def change_birthday(self, birthday: str) -> tuple:
        """Modify an existing user's birthday entry in the address book."""
        if not self.birthday:
            return False, f'Birthday not specified for \"{self.name.value}\". You can add it.'

        else:
            self.birthday = Birthday(birthday)
            return True,

    # def change_phone(self, ....):
    