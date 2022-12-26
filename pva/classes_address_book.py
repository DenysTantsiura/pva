from datetime import datetime, date  # date? where in use? build in datetime obj. not needed import, right?
import re
from typing import Union


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


class Address(Field):
    """Class of contact Adress."""

    @Field.value.setter
    def value(self, new_value: str) -> None:
        
        if re.search(r'ave', new_value) or re.search(r'str', new_value) or re.search(r'City', new_value) or re.search(r'city', new_value):
            self._value = new_value
        
        else:
            raise ValueError ('Wrong adress. Enter "City (name city) or (type street. Name street)"')
            
    def __str__(self) -> str:
        return f'{self.value}' if self.value else ''


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
        return f'{self.value.date()}' if self.value else 'Data in not value.'


class Email(Field):
    """Class of contact Email."""

    @Field.value.setter
    def value(self, new_value: str) -> None:
        
        if re.search(r'\b[a-zA-z][\w_.]+@[a-zA-z]+\.[a-zA-z]{2,}$', new_value) or\
            re.search(r'\b[a-zA-z][\w_.]+@[a-zA-z]+.[a-zA-z]+.[a-zA-z]{2,}$', new_value): 
            self._value = new_value

        # else:  
        #     raise ValueError('Email incorect. Try again.')
            # return '? Email incorect. Try again.'  # ??? print

class Name(Field):
    """Class of name contact."""   
    
    @Field.value.setter
    def value(self, value):
        if re.search(r"[a-zA-Zа-яА-Я']{2,}[\w-]{1,}", value):
            self._value = value.title()

        else: 
            raise ValueError ('Wrong name. Please input correct name')


class Phone(Field):
    """Class of number phone contact."""
    
    @Field.value.setter
    def value(self, value):
        new_value = self.preformatting(value)
        if re.search(r'[0-9]{10,12}', new_value):
            self._value = new_value
        else:
            raise ValueError ('Wrong phone. Please enter correct phone number.')

    @staticmethod
    def preformatting(value: str) -> str:
        new_value = (
        value.strip()
        .replace('+', '')
        .replace('(', '')
        .replace(')', '')
        .replace('-', '')
        )
        return new_value
    
class Record:
    """Record class of person information."""

    def __init__(self, name: str, *phones: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def __str__(self) -> str:
        return f'{self.name.value}, \nbirthday{self.birthday}, \nphone(s): {self.phones}, \naddress: {self.address}, \nemail(s): {self.emails}\n'

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
            self.birthday = Birthday(birthday)  # or None
            return True

        else:
            return False

    def add_phone(self, phone_new: str) -> bool:
        """Adds a new entry for the user's phone to the address book."""
        try:
            phone_new = Phone(phone_new)
        except ValueError:
            print(f'{phone_new} - wrong input. Please enter correct phone number.')
            return False

        for phone in self.phones:
            if phone_new.value == phone.value:
                return False
        print(f'{phone_new.value} add to contact')
        self.phones.append(phone_new)

        return True
    
    def add_email(self, email_new: str) -> tuple:
        """Adds a new entry for the user's email to the address book."""
        email_new_ = Email(email_new)
        if not email_new_.value:
            return False, f'Email: {email_new} - incorect.\n'

        for email in self.emails:
            if email_new_.value == email.value:
                return False, f'\"{email_new}\" already recorded for \"{self.name.value}\".\n'

        self.emails.append(email_new_)

        return True, f'Email: {email_new} for contact {self.name.value} added.\n'

    def change_address(self, new_address: str) -> tuple:
        """Modify an existing user's address entry in the address book."""
        if new_address:
            self.address = Address(new_address)  # Address() if wrong address : value = None
            
            return True

        else:
            return False, f'Address is missing!\"{new_address}\"'

    def change_birthday(self, birthday: str) -> tuple:
        """Modify an existing user's birthday entry in the address book."""
        self.birthday = Birthday(birthday)
        return True

    def change_phone(self, phone_to_change: str, phone_new: str) -> tuple:
        """Modify an existing user's phone entry in the address book."""
        phone_to_change = Phone.preformatting(phone_to_change)
        phone_new = Phone.preformatting(phone_new)
        verdict = False

        for phone in self.phones:
            if phone.value == phone_new:  # new number already in record
 
                return False, f'\"{phone_new}\" already recorded for \"{self.name.value}\"'

            if phone.value == phone_to_change:  # old number not exist in record
                verdict = True

        if not verdict:
            return verdict, f'\"{phone_to_change}\" already recorded for \"{self.name.value}\"'

        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_change:
                phone_new_to = Phone(phone_new)
                self.phones.remove(phone)
                self.phones.insert(index, phone_new_to)

                return True,

    def change_email(self, email_to_change: str, email_new: str) -> tuple:
        """Modify an existing user's email entry in the address book."""
        verdict = False

        for email in self.emails:
            if email.value == email_new:  # new email already in record
                return False, f'\"{email_new}\" already recorded for \"{self.name.value}\".'

            if email.value == email_to_change:  # old email not exist in record
                verdict = True

        if not verdict:
            return verdict, f'\"{email_to_change}\" not specified in the contact \"{self.name.value}\"'

        for index, email in enumerate(self.emails):
            if email.value == email_to_change:
                email_new_to = Email(email_new)
                if not email_new_to.value:
                    return False, f'Invalid email: {email_new}'
                    
                self.emails.remove(email)
                self.emails.insert(index, email_new_to)

                return True, f'Email {email_to_change} for contact {self.name.value} has changed on {email_new}.'

    def remove_address(self) -> Union[bool, None]:
        """Deleting an address entry from a user entry in the address book."""
        if self.address:
            self.address = None
            return True

    def remove_birthday(self) -> Union[bool, None]:
        """Deleting a birthday entry from a user entry in the address book."""
        if self.birthday:
            self.birthday = None
            return True
    
    def remove_phone(self, phone_to_remove: str) -> Union[bool, None]:
        """Deleting a phone entry from a user entry in the address book."""
        phone_to_remove = Phone.preformatting(phone_to_remove)

        for phone in self.phones:
            if phone.value == phone_to_remove:
                self.phones.remove(phone)
                print (f'Phone number {phone.value} was delate.\n')

                return True

        print(f'\"{phone_to_remove}\" not specified in the contact \"{self.name.value}\"')

    def remove_email(self, email_to_remove: str) -> bool:
        """Deleting an email entry from a user entry in the address book."""
        for email in self.emails:
            if email.value == email_to_remove:
                self.emails.remove(email)

                return True, f'Email {email_to_remove} for  contact {self.name.value} has delete.\n'

        return False, f'\"{email_to_remove}\" not specified in the contact \"{self.name.value}\".\n'


    def days_to_birthday(self) -> int:
        """Count the number of days until the next birthday of the user."""
        if self.birthday.value:

            user_day = datetime(year=datetime.now().date().year,
                                month=self.birthday.value.month,
                                day=self.birthday.value.day)

            days_left = user_day.date() - datetime.now().date()

            if days_left.days <= 0:

                user_day = datetime(year=datetime.now().date().year + 1,
                                    month=self.birthday.value.month,
                                    day=self.birthday.value.day)

                return (user_day.date() - datetime.now().date()).days

            return days_left.days
        
    def get_phones_list(self) -> list:
        """Get all phones in list."""
        phone_list = []
        for phone in self.phones:
            phone_list.append(phone.value)
        return phone_list
    
    def get_emails_str(self) -> str:
        """Get all emails in str."""
        emails_str = ''
        for email in self.emails:
            emails_str += f'{email.value} '
        return emails_str