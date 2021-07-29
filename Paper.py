class Paper:
    def __init__(self, title, description, link, date):
        self.title = title
        self.description = description
        self.link = link
        self.date = date

    def __dict__(self):
        return {
            'Title': self.title,
            'Description': self.description,
            'Link': self.link,
            'Date': self.date}