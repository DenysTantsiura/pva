from collections import UserDict

class NoteBook(UserDict):
    """Class of NoteBook"""

    def add_record(self, record: str) -> None:
        """Add new record in the notebook."""
        self.data[record.name] = record


    def iterrator(self, count: int) -> list:
        tags = []
        
        for record in self.data.values():

            tags.append(record)
            i += 1

            if i == count:

                yield tags
                tags = []
                i = 0

        if tags:
            yield tags



    def remove_record(self, name: str) -> None:
        """Remove record from notebook."""
        self.data.pop(name)

    def sort_by_tags(self) -> list:
        tags = []
        
        for tag in self.data.value():
            tags.



