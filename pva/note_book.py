from collections import UserDict


class NoteBook(UserDict):
    """Class of NoteBook."""

    def add_record(self, record: Note) -> None:
        """Add new record in the notebook."""
        self.data[record.name] = record

    def iterrator(self, count: int) -> list:
        """Return (count) records of all notebook."""
        tags = []
        counter = 0
        for record in self.data.values():

            tags.append(record)
            counter += 1

            if counter == count:

                yield tags
                tags = []
                counter = 0

        if tags:
            yield tags

    def remove_record(self, name: str) -> None:
        """Remove record from notebook."""
        self.data.pop(name)

    def sort_by_tags(self) -> list:
        """Return list of note-names sorted by tags."""
        tags = []

        for note in self.data.values():
            tags.extend(note.tags)

        tags = list(set(tags))
        tags.sort()

        return list(dict.fromkeys([note.name for tag in tags for note in self.data.values() if tag in note.tags]))
