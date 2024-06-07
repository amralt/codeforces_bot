class User:
    def __init__(self, chatId, username):
        self.chatId = chatId
        self.username = username

    @classmethod
    def get_from_db(self, row):
        """Создает объект из записи в БД"""
        return self(
            chatId=row[0],
            username=row[1]
        )
