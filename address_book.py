from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):
    """Class of Address Book """
    def __str__(self) -> str:
        # Не зовсім розумію що сюди потрібно дoдавати
        pass


    def add_record(self, record) -> None:
        """Adds a new record to the address book"""
        self.data[record.name.value] = record


    def show_happy_birthday(self, meantime: int) -> list:
        """Shows a list of contacts whose birthday is a specified number of days from the current date"""
        now_day = datetime.now()
        birthday_people = []
        for contact in self.data.values():
            if contact.birthday:
                b_day = contact.birthday.value
                days_for_b_day = (b_day - now_day).days
                if days_for_b_day < 0:
                    next_b_day = datetime(year = now_day.year + 1, month=b_day.month, day = b_day.day)
                    days_for_b_day = (next_b_day - now_day).days
                if meantime >= days_for_b_day:
                    birthday_people.append(contact)
        return birthday_people

    
    def __iter__(self):
        for key, value in self.data.items():
            yield key, value


    def iterator(self, n_count: int) -> list:
        """Output of the address book by pages"""
        page = []
        i = 0
        for record in self.data.values():
            page.append(record)
            i += 1

            if i == n_count:
                yield page
                page = []
                i = 0

        if page:
            yield page


    def remove_record(self, name: str) -> None:
        """Delete contact from address book"""
        del self.data[name]
        


