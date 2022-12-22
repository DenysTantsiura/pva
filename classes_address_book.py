from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Adress(Field):
    """Class of contact Adress."""

    @Field.value.setter
    def value(self, new_value: str) -> None:
        
        if re.search(r'ave', new_value) or re.search(r'str', new_value):
            self._value = new_value
        
        else:
            print('Wrong adress. Enter "Type street. Name street"')
            

class Birthday(Field):
    """Class of Birthday data."""

    @Field.value.setter
    def value(self, new_value: str) -> None:

        try:
            birthday_data = datetime.strptime(new_value, "%Y-%m-%d")

        except ValueError:
            raise ValueError('Data in not value. Enter numbers in format yyyy-mm-dd.')

        if birthday_data <= datetime.now():
            self._value = birthday_data 

    def __str__(self) -> str:

        try:
            return f'{self.value.date()}'

        except AttributeError:
            raise AttributeError('Date in not value. Date in a future.')


class Email(Field):
    """Class of contact Email."""

    @Field.value.setter
    def value(self, new_value: str) -> None:
        
        if re.search(r'\b[a-zA-z][\w_.]+@[a-zA-z]+\.[a-zA-z]{2,}$', new_value) or\
            re.search(r'\b[a-zA-z][\w_.]+@[a-zA-z]+.[a-zA-z]+.[a-zA-z]{2,}$', new_value): 
            self._value = new_value

        else:
            print('Email incorect. Try again.')

email = Birthday("1999-02-29")

print(email)