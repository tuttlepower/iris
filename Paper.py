from datetime import datetime
class Paper:
    def __init__(self, title, description, link, date=datetime.now().date(), logo='https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png'):
        self.title = title
        self.description = description
        self.link = link
        self.date = date
        self.logo = logo
