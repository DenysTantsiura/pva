from collections import UserDict
# from datetime import datetime, timedelta


class AddressBook(UserDict):
    """Class of Address Book."""
    def add_record(self, record) -> None:
        """Adds a new record to the address book."""
        
        self.data[record.name.value] = record

    def show_happy_birthday(self, meantime: int) -> list:
        """Shows a list of contacts whose birthday is a specified number of days from the current date."""
        
        birthday_people = []
        for contact in self.data.values():
            if contact.birthday and meantime >= contact.days_to_birthday():
                birthday_people.append(contact)
        return birthday_people
    
    def __iter__(self):
        for key, value in self.data.items():
            yield key, value

    #def iterator(self, n_count: int) -> list:
    #    """Output of the address book by pages."""
    #    
    #    page = []
    #    i = 0
    #    for record in self.data.values():
    #        page.append(record)
    #        i += 1
#
#            if i == n_count:
#                yield page
#                page = []
#                i = 0
#
#        if page:
#            yield page

    def remove_record(self, name: str) -> None:
        """Delete contact from address book."""
        
        del self.data[name]
