from keep_alive import keep_alive
keep_alive()


import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import datetime
import sys

bot_token = '6277201027:AAEtUJEMIeW79_nTaJCzgRcHNErZGpdyi_Y'
bot = telebot.TeleBot(bot_token)

allowed_group_id = ""
allowed_users = []
processes = []
ADMIN_ID = 'gzlcuteso1thegioi'

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()


def TimeStamp():
  now = str(datetime.date.today())
  return now


def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
      '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()


print("Bot đã được khởi động thành công")


def add_user(message):
  admin_id = message.from_user.id
  if admin_id != ADMIN_ID:
    bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY😾.')
    return

  if len(message.text.split()) == 1:
    bot.reply_to(message, ' VUI LÒNG NHẬP ID NGƯỜI DÙNG ')
    return

  user_id = int(message.text.split()[1])
  allowed_users.append(user_id)
  expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
  connection = sqlite3.connect('user_data.db')
  save_user_to_database(connection, user_id, expiration_time)
  connection.close()

  bot.reply_to(
      message,
      f'🚀NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /supersms.🚀'
  )


load_users_from_database()


@bot.message_handler(commands=['get'])
def get(message):
  bot.reply_to(message, text='Vui lòng chò')

  with open('key.txt', 'a') as f:
    f.close()

  username = message.from_user.username
  string = f'GL-{username}+{TimeStamp()}'
  hash_object = hashlib.md5(string.encode())
  key = str(hash_object.hexdigest())
  print(k)
  url_key = requests.get(
      f'https://link4m.co/api-shorten/v2?api=64db7707c856714124120b3d&url=yourdestinationlink.com{key}'
  ).json()['shortenedUrl']

  text = f'''

 {key} 


    '''
  bot.reply_to(message, text)


@bot.message_handler(commands=['k'])
def k(message):
  if len(message.text.split()) == 1:
    bot.reply_to(message, 'sử dụng /get để lấy key')
    return

  user_id = message.from_user.id

  key = message.text.split()[1]
  username = message.from_user.username
  string = f'GL-{username}+{TimeStamp()}'
  hash_object = hashlib.md5(string.encode())
  expected_key = str(hash_object.hexdigest())
  if key == expected_key:
    allowed_users.append(user_id)
    bot.reply_to(
        message,
        'Key hợp lệ'
    )
  else:
    bot.reply_to(
        message,
        'Key không hợp lệ')


@bot.message_handler(commands=['fb'])
def lqm_sms(message):
  user_id = message.from_user.id
  if user_id not in allowed_users:
    bot.reply_to(
        message,
        text=
        'Hãy /get để lấy key sử dụng lệnh này'
    )
    return
  if len(message.text.split()) == 1:
    bot.reply_to(message, 'Vui lòng nhập link hoặc id fb ')
    return

  phone_number = message.text.split()[1]

  file_path = os.path.join(os.getcwd(), "info.py")
  process = subprocess.Popen(["python", file_path, phone_number, "120"])
  processes.append(process)
  bot.reply_to(
      message,
      f'Vui lòng chờ...'
  )


@bot.message_handler(commands=['start'])
def how_to(message):
  how_to_text = '''
 Cách sử dụng và All lệnh của Bot:
- Sử dụng lệnh /get để lấy key.
- Khi lấy key xong, sử dụng lệnh /k {key của bạn} để xác định key.
( ví dụ: /key keycuaban )
- /fb <link hoặc id facebook>: Check thông tin facebook (chỉ người dùng được phép).
- /status: Xem thông tin về thời gian hoạt động, % CPU, % Memory, % Disk đang sử dụng của bot.
- /stop: Dừng lại tất cả các tác vụ đang chạy. ( Chỉ Quản Trị Viên Mới Được Dùng Lệnh Này).
-/restart: Khởi động lại bot (Chỉ admin).
- /admin: Hiển thị thông tin admin.
- /help: danh sách lệnh và hướng dẫn sử dụng.
'''
  bot.reply_to(message, how_to_text)




@bot.message_handler(commands=['help'])
def help(message):
  help_text = '''
 Danh sách lệnh:
- /get : Lấy key sử dụng bot
- /fb <link hoặc id facebook>: Check thông tin facebook (chỉ người dùng được phép).
- /k "key của bạn": Kiểm tra key và xác nhận quyền sử dụng lệnh /fb.
- /status: Xem thông tin về thời gian hoạt động, % CPU, % Memory, % Disk đang sử dụng của bot.
- /stop: Dừng lại tất cả các tác vụ đang chạy. ( Chỉ Quản Trị Viên Mới Được Dùng Lệnh Này).
-/restart: Khởi động lại bot (Chỉ admin).
- /admin: Hiển thị thông tin admin.
'''
  bot.reply_to(message, help_text)


@bot.message_handler(commands=['admin'])
def how_to(message):
  how_to_text = '''
 Thông Tin Admin:
- Nguyễn Thành Khai x Trần Thanh Tâm
🚀Thông Tin Liên Hệ ☎️:🚀
- Owner Telegram: https://t.me/gzlcuteso1thegioi
- Zalo: https://zalo.me/0348560360
- Facebook: https://facebook.com/ntk.sad
'''
  bot.reply_to(message, how_to_text)



@bot.message_handler(commands=['status'])
def status(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này😾.')
    return
  if user_id not in allowed_users:
    bot.reply_to(message, text='Bạn không có quyền sử dụng lệnh này😾.')
    return
  process_count = len(processes)
  bot.reply_to(message, f'Số quy trình đang xử lý {process_count}.')


@bot.message_handler(commands=['restart'])
def restart(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Đã khởi động lại bot')
    return

  bot.reply_to(message, 'Bot sẽ được khởi động lại sau 3s')
  time.sleep(2)
  python = sys.executable
  os.execl(python, python, *sys.argv)


@bot.message_handler(commands=['stop'])
def stop(message):
  user_id = message.from_user.id
  if user_id != ADMIN_ID:
    bot.reply_to(message, 'Bạn không có quyền Admin')
    return

  bot.reply_to(message, 'Đã dừng bot')
  time.sleep(2)
  bot.stop_polling()


bot.polling()
