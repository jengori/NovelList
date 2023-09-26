# This class is responsible for organising data returned by the ApiHandler class list_names_call method
class NamesDataHandler:

    def __init__(self, data: dict):
        self.data = data

    def get_frequency(self, encoded_category: str):
        return "".join([self.data[i]['updated']
                        for i in range(len(self.data)) if self.data[i]['list_name_encoded'] == encoded_category])

    def get_start_date(self, encoded_category: str):
        return "".join([self.data[i]['oldest_published_date']
                        for i in range(len(self.data)) if self.data[i]['list_name_encoded'] == encoded_category])

    def get_end_date(self, encoded_category: str):
        return "".join([self.data[i]['newest_published_date']
                       for i in range(len(self.data)) if self.data[i]['list_name_encoded'] == encoded_category])


# This class is responsible for organising data returned by the ApiHandler class lists_call method
class ListsDataHandler:

    def __init__(self, data: dict):
        self.data = data

    def get_title(self, index):
        return self.data[index]['title']

    def get_author(self, index):
        return self.data[index]['author']

    def get_description(self, index):
        return self.data[index]['description']

    def list_entry_string(self, index):
        return f"{index+1}. {' ' if index<9 else ''}{self.get_title(index)}, {self.get_author(index)}"
