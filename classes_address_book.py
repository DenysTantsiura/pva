from datetime import datetime, date
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

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str):
        
        if re.search(r"ave", new_value) or re.search(r"str", new_value):
            self._value = new_value
        
        else:
            print('Wrong adress. Enter "Type street. Name street"')
            

class Birthday(Field):
    """Class of Birthday data."""

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str):

        try:
            birthday_data = datetime.strptime(new_value, "%Y-%m-%d")

        except ValueError:
            raise ValueError('Data in not value. Enter numbers in format yyyy-mm-dd.')

        if birthday_data <= datetime.now():
            self._value = birthday_data 
        
        else:
            print('Person not born')
        
    def __str__(self) -> str:

        try:
            return f'{self.value.date()}'
        except AttributeError:
            AttributeError('Person not born')


class Email(Field):
    """Class of contact Email."""

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str):
        
        if re.search(r'\b[a-zA-z][\w_.]+@[a-zA-z]+\.[a-zA-z]{2,}$', new_value): 
            self._value = new_value
        else:
            print('Email incorect. Try again.')