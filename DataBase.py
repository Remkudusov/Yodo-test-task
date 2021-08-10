import psycopg2

class DataBase:

    def __init__(self):
        self.connection = psycopg2.connect(host="localhost", port = 5432, database="WhatsAppDB", user="rem_dev", password="12345678")
        self.cursor = self.connection.cursor()

    def save_chat(self, id, token, instanceId):
        self.cursor.execute("""INSERT INTO free_chats(id, token, instance_id) VALUES ({0}, \'{1}\', \'{2})\');""".format(id, token, instanceId))
        self.connection.commit()

    def get_chats(self):
        self.cursor.execute("""SELECT * FROM free_chats""")
        return self.cursor.fetchall()

    def save_user(self, phone, name):
        self.cursor.execute("""INSERT INTO user_data(phone, name) VALUES (\'{0}\', \'{1}\');""".format(phone, name))
        self.connection.commit()

    def get_users(self):
        self.cursor.execute("""SELECT * FROM user_data""")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()