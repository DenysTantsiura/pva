from collections import UserDict


class AddressBook(UserDict):
    """Class of Address Book."""
    def add_record(self, record) -> None:
        """Adds a new record to the address book."""

        self.data[record.name.value] = record

    def show_happy_birthday(self, meantime: int) -> list:
        """Shows a list of contacts whose birthday is a specified number of days from the current date."""

        birthday_people = ''
        try:
            meantime = int(meantime)
        except ValueError:
            raise ValueError('Command \'happy birthday\' shows users whose birthday is in a given range of days. Please enter range of days. Example:\nhappy birthday <days>')
        for contact in self.data.values():
            if contact.birthday and contact.birthday.value and int(meantime) >= contact.days_to_birthday():
                birthday_people += f'{contact.name.value}\'s birthday: {contact.birthday.value.date()}\n'
        return birthday_people[:-1]

    def iterator(self, count: int) -> list:
        """Output of the address book by pages."""
        current_pages = 0
        dictionary_iterator = iter(self.data)

        while current_pages < len(self.data):
            page = []
            for i in range(count):
                try:
                    page.append(self.data[next(dictionary_iterator)])

                except StopIteration:
                    current_pages = len(self.data)

            yield page

            current_pages += count

    def remove_record(self, name: str) -> None:
        """Delete contact from address book."""

        del self.data[name]
