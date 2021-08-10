from WhatsAppApi import WhatsAppAPI
from DataBase import DataBase

whats_app = WhatsAppAPI(318002)
db = DataBase()

# Получить свободный чат и записать данные в базу
chat_info = whats_app.get_chat()
print(chat_info)
db.save_chat(chat_info['id'], chat_info['token'], chat_info['instanceId'])

# Получить QR код
whats_app.get_qr()

# Получить статус что вацап подключен и записать имя и телефон
account_info = whats_app.get_account_info()
print(account_info)
db.save_user(account_info['phone'], account_info['name'])

# Отправить сообщение
whats_app.send_message('79773554865', "Отправляю тебе это сообщение через WhatsApp API")

db.close()