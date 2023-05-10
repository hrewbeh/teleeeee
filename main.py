import telebot
import pytube
from bs4 import BeautifulSoup
import requests
from config import TOKKEN_TELEGRAM

bot = telebot.TeleBot(token=TOKKEN_TELEGRAM)
@bot.message_handler(commands=["video"])
def send_video(message):
	url = message.text.split(' ')[1]
	responce = requests.get(url)
	soup = BeautifulSoup(responce.text, 'html.parser')
	title = soup.title.string
	youtube = pytube.YouTube(url)
	streams = youtube.streams.filter(progressive=True, file_extension='mp4').first()
	
	streams.download()
	
	with open(streams.default_filename, 'rb') as video:
		bot.send_video(chat_id=message.from_user.id, video=video, caption=title)
		
	# bot.send_message(chat_id=message.from_user.id, text=soup)


if __name__ == '__main__':
	bot.polling(non_stop=True)
	
