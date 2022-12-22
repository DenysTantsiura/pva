class Note:
    def __init__(self, name: str, text: str) -> None:
        '''__init__...": The bot initializes an object of the Notes class and creates list of tags.
       
        Parameters:
            name (str): name of the note.
            text (str): Instance of AddressBook.'''
        
        self.name = name
        self.text = text
        self.tags = []

    def __str__(self) -> str:
        return f'{self.name}: {self.text}'

    def add_tags(self, new_tags: str) -> tuple:
        '''add_tags...": The bot adds a new tag or tags to list of tags. 
        The bot takes into account the limit of the number of tags.
        Parameters:
            new_tags (str): Tags that the user wants to add.
        Returns:
            string(str): If false - the answer for the user, otherwise - a list of tags.'''

        add_tags = new_tags.split(', ')
        number_tags = 5
        if len(self.tags) > number_tags:
            return ('You cannot add more than five tags!')
        else:
            delta = number_tags - len(self.tags)
            if len(add_tags) <= delta:
                for tag in add_tags:
                    if tag in self.tags:
                        return ('This tag already exists!')
                    else:   
                        self.tags.append(', '.join(add_tags))
                        return self.tags
            else:
                return (f'You can add only {delta} tags!')
   
    def change_note(self, changed_text, new_text) -> tuple:
        '''change_note...": The bot rewrites note or changes some words.
        Parameters:
            changed_text (str): The text the user wants to change.
            new_text (str): The new text the user wants to add.
        Returns:
            self.text: Changed text.'''

        if self.text == changed_text:
            self.text = new_text
        else:
            self.text = self.text.replace(changed_text, new_text)
        print(f'{self.name}: {self.text}')
        return self.text
       
