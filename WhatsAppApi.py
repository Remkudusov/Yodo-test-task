import requests
import ast
import base64
import time
from PIL import Image

class WhatsAppAPI:

    def __init__(self, instant_id):
        self.instant_id = instant_id

        with open("token.txt", 'r') as f:
            self.token = f.readline()

        with open("X-Whatsapp-Token.txt", 'r') as f:
            self.X_Whatsapp_Token = f.readline()

        self.headers = {'X-Whatsapp-Token': self.X_Whatsapp_Token}

    def get_chat(self):
        url = 'https://dev.whatsapp.sipteco.ru/v3/chat/spare?crm=HUBSPOT'

        response = requests.get(url, headers=self.headers)
        answer = ast.literal_eval(response.text)

        return answer

    def get_qr(self):
        url = 'https://api.chat-api.com/instance' + str(self.instant_id) + '/status?token=' + str(self.token)

        response = requests.get(url, headers=self.headers, stream=True)
        answer = ast.literal_eval(response.text)
        img_code = (answer['qrCode'].split(','))[1]
        img_data = base64.b64decode(img_code)

        with open("qr_code.png", 'wb') as f:
            f.write(img_data)

        im = Image.open("qr_code.png")
        im.show()

    def get_account_info(self):
        instance_url = 'https://api.chat-api.com/instance' + str(self.instant_id) + '/status?token=' + str(self.token)

        instance_response = requests.get(instance_url, headers=self.headers)
        instance_answer = ast.literal_eval(instance_response.text)

        user_info = {}

        while instance_answer['accountStatus'] != 'authenticated':
            print("Осуществляется попытка пройти авторизацию")
            time.sleep(5)
            instance_response = requests.get(instance_url, headers=self.headers)
            instance_answer = ast.literal_eval(instance_response.text)

        print("Пользователь успешно авторизован")
        user_url = 'https://api.chat-api.com/instance' + str(self.instant_id) + '/me?token=' + str(self.token)

        user_response = requests.get(user_url, headers=self.headers)
        user_answer = ast.literal_eval(user_response.text)

        user_info['phone'] = (user_answer['id'].split('@'))[0]
        user_info['name'] = user_answer['name']

        return user_info

    def send_message(self, phone, text):
        url = 'https://api.chat-api.com/instance' + str(self.instant_id) + '/sendMessage?token=' + str(self.token)
        payload = {'body': text, 'phone': phone}

        response = requests.post(url, data=payload)
        print(response.text)

    def __str__(self):
        return self.token