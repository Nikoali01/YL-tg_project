import sqlite3


class dbworker:
    def __init__(self, database_name):
        ''' Констуктор '''
        self.connection = sqlite3.connect("db dumb1.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def chat_exists(self, new_chat_id):
        ''' Проверка есть ли chat в бд '''
        with self.connection:
            sqlite_select_query = """SELECT * FROM users"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            for i in records:
                if i[2] == new_chat_id:
                    return 1
            return 0

    def add_chat(self, telegram_id, chat_id):
        '''Добавляем новый чат'''
        with self.connection:
            self.new_chat_id = chat_id
            self.tg_id = telegram_id
            self.cursor.execute('UPDATE `users` SET `chat_id` = ? WHERE `telegram_id` = ?', (chat_id, telegram_id))
            self.connection.commit()
            self.cursor.execute('UPDATE `users` SET `activity` = ? WHERE `telegram_id` = ?', (1, telegram_id))
            self.connection.commit()
            return 1

    def getting_all_chats(self, ids):
        '''собираем инфу о всех чатах'''
        with self.connection:
            sqlite_select_query = """SELECT * FROM users"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            for i in records:
                print(i)
        return 1

    def giving_activity(self, telegram_id, chat_id):
        '''придаём активность(0/1)'''
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `activity` = ? WHERE `telegram_id` = ?', (1, telegram_id))
            self.connection.commit()
            self.cursor.execute('UPDATE `users` SET `chat_id` = ? WHERE `telegram_id` = ?', (chat_id, telegram_id))
            self.connection.commit()
            return 1

    def exit(self, telegram_id):
        '''выход с чата'''
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `chat_id` = ? WHERE `telegram_id` = ?', ("NULL", telegram_id))
            self.connection.commit()
            self.cursor.execute('UPDATE `users` SET `activity` = ? WHERE `telegram_id` = ?', (0, telegram_id))
            self.connection.commit()

    def delliting(self):
        '''удаление аккаунта'''
        with self.connection:
            sql = """DELETE FROM users WHERE telegram_id = 406649546"""
            self.cursor.execute(sql)
            self.connection.commit()
            print(2)
            sqlite_select_query = """SELECT * FROM users"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            for i in records:
                print(i)
            return 1

    def getting_act(self, telegram_id):
        '''получение активности(проверка)'''
        with self.connection:
            result = self.cursor.execute('SELECT `activity` FROM `users` WHERE `telegram_id` = ?',(telegram_id,)).fetchone()
            print(result)
            if result == 1:
                return 1
            else:
                return 0

    def giving_chat(self, telegram_id):
        '''добавляем чат к аккаунту'''
        with self.connection:
            sql = """DELETE FROM users WHERE telegram_id = telegram_id"""
            self.cursor.execute(sql)
            self.connection.commit()
            return 1

    def user(self, telegram_id):
        '''запись в юзеры'''
        with self.connection:
            self.cursor.execute("INSERT INTO users (telegram_id) VALUES(?)",
                                (telegram_id,))
            self.connection.commit()

    def getting_chat(self, telegram_id):
        '''получение чата, в котором пользователь'''
        with self.connection:
            result = self.cursor.execute('SELECT `chat_id` FROM `users` WHERE `telegram_id` = ?',
                                         (telegram_id,)).fetchone()
            ah = result
            return result

    def getting_connected(self, ah):
        '''получаем список подключенных пользователей'''
        with self.connection:
            spis = []
            sqlite_select_query = """SELECT * FROM users"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            for i in records:
                if i[2] == ah:
                    spis.append(i[1])
            return spis