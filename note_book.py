from collections import UserDict

class NoteBook(UserDict):
    """Class of NoteBook"""

    def add_record(self, record: str) -> None:
        """Add new record in the notebook."""
        self.data[record.name] = record

    def iterrator(self):
        pass

    def remove_record(self, name: str) -> None:
        """Remove record from notebook."""
        self.data.pop(name)

    def sort_by_tags(self) -> list:
        pass

note = NoteBook()

print(note.add_record("illia", "illia work"))