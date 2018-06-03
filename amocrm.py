#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
# sys.setdefaultencoding() does not exist, here!
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')
# -*- coding: utf-8 -*-
import telebot
from time import sleep
import constants
import sys
import logging
import requests
import json
from datetime import datetime
from pytz import timezone
from time import mktime
import os
from math import ceil
import flask

API_TOKEN = constants.token
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN)
s = requests.Session()
user_dict = {}
bot = telebot.TeleBot(constants.token)
postdata = {'USER_HASH': constants.hash, 'USER_LOGIN':constants.login }
r = s.post('https://dbp.amocrm.ru/', data=postdata)
print (r.status_code)

query_dict={}
user_kp_dict={}

postdata = {'USER_HASH': constants.hash, 'USER_LOGIN':constants.login }
r = s.post('https://dbp.amocrm.ru/', data=postdata)
print (r.status_code)

WEBHOOK_HOST = '46.101.124.15'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = 'amocrm/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'amocrm/webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


app = flask.Flask(__name__)



@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


fmt = "%Y-%m-%d %H:%M:%S %Z%z"
time_zone='Asia/Almaty'
current="%Y-%m-%d"

def validate_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        current_time=now_time.strftime(current)
        if(d>current_time):
            return True
        else:
            return False
    except ValueError:
        return False
now_time = datetime.now(timezone(time_zone))
unix_time_now = (mktime(datetime.now().timetuple()))
human_time_now = (now_time.strftime(fmt))
print (unix_time_now)
print (human_time_now)
good=[200,201,202,203, 204,205,206,207 ,208,226]
global_row2=[telebot.types.InlineKeyboardButton(u"\U0001F519"+" Назад",callback_data=("/back")),telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Поиск",callback_data=("/search"))]
					
nazad_v_menu=telebot.types.ReplyKeyboardMarkup(True,False)
nazad=u"\U0001F519"+" Назад в меню"
nazad_v_menu.row()



class Query:
    def __init__(self, query):
        self.query = query
class User:
    def __init__(self, name):
        self.name = name
        self.ID = None
        self.email = None
        self.phone = None
        self.TOO = None

class Takekp:
    def __init__(self, code):
        self.code = code
        self.kol = None
        self.address= None
        self.date = None
        
def check_contact(message):
	global good
	global s
	global r
	global postdata
	try:
		check_contact=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list?query='+str(message)+'&type=contact')# Поиск по ID
		if check_contact.status_code in good:
			#bot.send_message(295091909,r.status_code)
			return len(check_contact.content)>0
			'''
			name = check_contact.json()
			user_id=name['response']['contacts'][0]['name']
			if user_id==str(message):
				return name['response']['contacts'][0]['custom_fields'][1]['values'][0]['value']
			else:
				return False
			'''	
		else:
			#bot.send_message(295091909,r.status_code)
			s = requests.Session()
			r = s.post('https://dbp.amocrm.ru/', data=postdata)
			check_contact=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list?query='+str(message)+'&type=contact')# Поиск по ID
			return len(check_contact.content)>0
		#bot.send_message(295091909,r.status_code)
		
	except Exception as e:
		bot.send_message(295091909,str(e)+' check_contact :')

def check_follow(message): # Временно отключить
	check_contact = s.get('https://dbp.amocrm.ru/private/api/v2/json/customers/list?term='+str(message))# Поиск по ID
	print (check_contact.status_code)
	data=check_contact.json()
	print(data)
	next_date=data['response']['customers'][0]['next_date']
	print(next_date)
	current_time = int(mktime(datetime.now(timezone(time_zone)).timetuple()))
	return (next_date-current_time>0)


@bot.message_handler(commands=['start'])
def starting(message):
	print(message.text)
	have_user=check_contact(message.from_user.id)
	if have_user:
		next_prev_markup = telebot.types.InlineKeyboardMarkup()
		row=[telebot.types.InlineKeyboardButton(u"\U0001F4E3"+" заказать КП",callback_data="/takekp")]
		row2=[telebot.types.InlineKeyboardButton(u"\U0001F4DD"+" Найти аналог",callback_data="/searchsame")]
		row4=[telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Поиск товара",callback_data="/search")]
		next_prev_markup.row(*row)
		next_prev_markup.row(*row2)
		next_prev_markup.row(*row4)
		bot.send_message(message.from_user.id,"С возвращением !")
		bot.send_message(message.from_user.id,"Вы в главном меню "+u"\U0001F3AF"+"\n\n" + "* Для поиска продукта нажмите на кнопку \n[ "+u"\U0001F50D"+" Поиск товара ]\n* Для запроса аналога продукта нажмите на кнопку \n[ "+u"\U0001F4DD"+" Найти аналог ]\n * Для запроса КП нажмите на кнопку \n[ "+u"\U0001F4E3"+" заказать КП ]", reply_markup=next_prev_markup)
		
	else:
		#print ('[STARTED Conversation V2 empty]')
		#print (message.from_user.id)
		bot.send_message(message.from_user.id,'Для начала работы вам необходимо пройти регистрацию, все данные будут использоваться для составления КП, так что проверяйте на правильность введенных данных')
		msg = bot.send_message(message.from_user.id, "Введите ваши ФИО")
		bot.register_next_step_handler(msg, process_name_step)
def process_name_step(message):
    try:
        chat_id = message.from_user.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg =  bot.send_message(chat_id, 'Введите ваш ИИН')
        bot.register_next_step_handler(msg, process_ID_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так, Process_name')
def process_ID_step(message):
    try:
        chat_id = message.from_user.id
        ID = message.text
        if not ID.isdigit():
            msg =  bot.reply_to(message, 'ИИН должен состоять из цифр')
            bot.register_next_step_handler(msg, process_ID_step)
            return
        user = user_dict[chat_id]
        user.ID = ID
        msg =  bot.send_message(chat_id, 'Введите вашу почту')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так, Process_ID')
def process_email_step(message):
    try:
        chat_id = message.from_user.id
        email = message.text
        user = user_dict[chat_id]
        user.email = email
        msg = bot.send_message(chat_id, 'Введите ваш телефон')
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так, Process_Email')
def process_phone_step(message):
    try:
        chat_id = message.from_user.id
        phone = message.text
        user = user_dict[chat_id]
        user.phone = phone
        msg =  bot.send_message(chat_id, 'Введите ваше ТОО\ИП')
        bot.register_next_step_handler(msg, process_TOO_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так, Process_Phone')
def process_TOO_step(message):
	try:
		chat_id = message.from_user.id
		TOO = message.text
		user = user_dict[chat_id]
		user.TOO = TOO
		print (user.name,user.ID,user.phone,user.email,user.TOO)
		bot.send_message(chat_id,"Ожидайте...")
		postdata = {
				"request":  {
					"contacts":  {
						"add":  
							[{
								"name":  chat_id,
								"tags": "клиент",
								"custom_fields":  
								[
									{
										"id":  384511,
										"name": "ИИН",
										"values":  [
										{
										"value":  user.ID
										},

													]
									},
									
									{
										"id":  384515,
										"name": "ФИО",
										"values":  [
										{
										"value":  user.name
										},

													]
									},

									{
										"id":  386421,
										"name": "Компания",
										"values":  [
										{
										"value":  user.TOO
										},

													]
									},
									{
										"id":  313537,
										"name": "Раб. тел.",
										"code": "PHONE",
										"values":  [
										{
										"value":  user.phone,
										"enum":"649801"
										},

													]
									},
									{
										"id":  313539,
										"name": "Email",
										"code": "EMAIL",
										"values":  [
										{
										"value":  user.email,
										"enum":"649813"
										},

													]
									},
								
								]
							}]
						}
					}
				}
		post_contact = s.post('https://dbp.amocrm.ru/private/api/v2/json/contacts/set',data=json.dumps(postdata))
		print (post_contact.status_code)
		print (post_contact.content)
		contact_id=(post_contact.json()['response']['contacts']['add'][0]["id"])
		print (contact_id)
		customer={"request": {
					"customers": {
						"add": [
							{
							"main_user_id":1768789,
							"name":chat_id,
							"next_price":0,
							"next_date":unix_time_now+864000,
								}
								],
								}}}
		post_customer = s.post('https://dbp.amocrm.ru/private/api/v2/json/customers/set',data=json.dumps(customer))
		customer_id=(post_customer.json()['response']['customers']['add']['customers'][0]["id"])
		customer_set_contact={
								"request": {
								"links": {
								"link": [
								{
								"from": "customers",
								"to": "contacts",
								"from_id": customer_id,#customer_id
								"to_id": contact_id # contact_id
								}
								]
								}
								}
								}
		customer_to_lead = s.post('https://dbp.amocrm.ru/private/api/v2/json/links/set',data=json.dumps(customer_set_contact))
		if post_customer.status_code==200 and post_contact.status_code==200:
			bot.send_message(chat_id,"Регистрация успешно пройдена! Приятного использования")
			next_prev_markup = telebot.types.InlineKeyboardMarkup()
			row=[telebot.types.InlineKeyboardButton(u"\U0001F4E3"+" заказать КП",callback_data="/takekp")]
			row2=[telebot.types.InlineKeyboardButton(u"\U0001F4DD"+" Найти аналог",callback_data="/searchsame")]
			row4=[telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Поиск товара",callback_data="/search")]
			next_prev_markup.row(*row)
			next_prev_markup.row(*row2)
			next_prev_markup.row(*row4)

			bot.send_message(message.from_user.id,"Вы в главном меню "+u"\U0001F3AF"+"\n\n" + "* Для поиска продукта нажмите на кнопку \n[ "+u"\U0001F50D"+" Поиск товара ]\n* Для запроса аналога продукта нажмите на кнопку \n[ "+u"\U0001F4DD"+" Найти аналог ]\n * Для запроса КП нажмите на кнопку \n[ "+u"\U0001F4E3"+" заказать КП ]", reply_markup=next_prev_markup)
			#bot.send_message(chat_id,"База данных поставщиков доступна при первой регистрации только 10 дней, дальнейшее использование поиском базы осуществляется по подписке. Оформить подписку сразу можно командой /pay")	
		else:
			bot.send_message(chat_id,"Система не смогла зарегестрировать вас, прошу сделать запрос позже...")
			bot.send_message(295091909,":NOT ERROR REGISTRATION STEP\nFrom user: @"+message.from_user.username+"\nFROM ID: "+message.from_user.id+"\ninfo:"+user.name+", "+user.ID+", "+user.phone+", "+user.email+", "+user.TOO+"\nADDITIONAL: "+post_contact.status_code+" = status, content = "+post_contact.content+", text = "+r.text)

	except Exception as e:
		#print(e)
		bot.send_message(message.from_user.id,"Система не смогла зарегестрировать вас, прошу сделать запрос позже...")
		bot.send_message(295091909,str(e)+": REGISTRATION STEP\nFrom user: "+message.from_user.username+"\nFROM ID: "+message.from_user.id+"\ninfo:"+user.name+", "+user.ID+", "+user.phone+", "+user.email+", "+user.TOO+"\nADDITIONAL: "+post_contact.status_code+" = status, content = "+post_contact.content+", text = "+r.text)

		

		#bot.reply_to(message, "Система не смогла зарегестрировать вас, прошу сделать запрос позже...")



@bot.message_handler(commands=['searchproduct'])
def searchproduct(message):
	print(message.text)
	have_user=check_contact(message.from_user.id)
	if have_user:
		msg = bot.send_message(message.from_user.id, "Введите полную техническую спецификацию продукта ")
		bot.register_next_step_handler(msg, process_searchproduct_step)
	else:
		print ('Не зареган')
		print (message.from_user.id)
		bot.send_message(message.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')





@bot.message_handler(commands=['search'])
def starting(message):
	print(message.text)
	have_user=check_contact(message.from_user.id)
	if have_user:
		msg = bot.send_message(message.from_user.id, "Введите ключевые слова (например марку или модель продукта) что бы найти её в базе поставщиков.")
		bot.register_next_step_handler(msg, process_search_step)
	else:
		print ('Не зареган')
		print (message.from_user.id)
		bot.send_message(message.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')

@bot.message_handler(commands=['takekp'])
def starting_takekp(message):
	print(message.text)
	have_user=check_contact(message.from_user.id)
	if have_user:
		bot.send_message(message.from_user.id,"Введите информацию которую сейчас у вас запросит бот")
		msg = bot.send_message(message.from_user.id, "Код товара поставщика")
		bot.register_next_step_handler(msg, process_code_step)
	else:
		print ('не зареган')
		print (message.from_user.id)
		bot.send_message(message.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')


@bot.message_handler(commands=['searchsame'])
def searchsame(call):
	print(call.text)
	have_user=check_contact(call.from_user.id)
	if have_user:
		msg = bot.send_message(call.from_user.id, "Введите полную техническую спецификацию продукта ")
		bot.register_next_step_handler(msg, process_searchsame_step)
	else:
		print ('Не зареган')
		print (call.from_user.id)
		bot.send_message(call.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')




@bot.callback_query_handler(func=lambda call: call.data == '/back')
def back(call):
	print(call.data)
	have_user=check_contact(call.from_user.id)				
	if have_user:
		next_prev_markup = telebot.types.InlineKeyboardMarkup()
		row=[telebot.types.InlineKeyboardButton(u"\U0001F4E3"+" заказать КП",callback_data="/takekp")]
		row2=[telebot.types.InlineKeyboardButton(u"\U0001F4DD"+" Найти аналог",callback_data="/searchsame")]
		row4=[telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Поиск товара",callback_data="/search")]
		next_prev_markup.row(*row)
		next_prev_markup.row(*row2)
		next_prev_markup.row(*row4)
		#bot.edit_message_text(temp_response, call.from_user.id, call.message.message_id, reply_markup=next_prev_markup)
		bot.edit_message_text("Вы в главном меню "+u"\U0001F3AF"+"\n\n" + "* Для поиска продукта нажмите на кнопку \n[ "+u"\U0001F50D"+" Поиск товара ]\n* Для запроса аналога продукта нажмите на кнопку \n[ "+u"\U0001F4DD"+" Найти аналог ]\n * Для запроса КП нажмите на кнопку \n[ "+u"\U0001F4E3"+" заказать КП ]", call.from_user.id, call.message.message_id,reply_markup=next_prev_markup)
		#Error
	else:
		print ('Не зареган')
		print (call.from_user.id)
		bot.send_message(call.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')
@bot.callback_query_handler(func=lambda call: call.data[:12] == 'limit_offset')
def next(call):
	global global_row2
	temp=call.data.split(":")
	next_prev_markup = telebot.types.InlineKeyboardMarkup()
	prev_=int(temp[1])-10
	next_=int(temp[1])+10
	query_sum=int(temp[2])
	query=temp[3]
	row=[]
	row.append(telebot.types.InlineKeyboardButton(u"\u2B05",callback_data=("limit_offset:"+str(prev_)+":"+str(query_sum)+":"+query)))
	row.append(telebot.types.InlineKeyboardButton(u"\u27A1",callback_data=("limit_offset:"+str(next_)+":"+str(query_sum)+":"+query)))
	next_prev_markup.row(*row)
	next_prev_markup.row(*global_row2)
	try:
		print (prev_)
		print (next_)
		if prev_<-10 or next_>=query_sum+10:
			bot.answer_callback_query(call.id, text=u"\U0001F644")
		else:
			response=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list/?query='+query+'&limit_rows=10&limit_offset='+str(int(temp[1])))# Поиск по контрактам
			data = response.json()
			temp_response=''
			data_count=len(data['response']['contacts'])
			if data_count<=10:
				for i in range(data_count):
					temp_response+=str(i+int(temp[1])+1)+') '+data['response']['contacts'][i]['name']+'( /'+str(data['response']['contacts'][i]['id'])+' )\n'
			else:
				for i in range(10):
					temp_response+=str(i+int(temp[1])+1)+') '+data['response']['contacts'][i]['name']+'( /'+str(data['response']['contacts'][i]['id'])+' )\n'

			bot.edit_message_text(temp_response, call.from_user.id, call.message.message_id, reply_markup=next_prev_markup)
			bot.answer_callback_query(call.id, text="")
	except:
		bot.answer_callback_query(call.id, text=u"\U0001F644")
		bot.send_message(call.from_user.id,"Сначала создайте запрос по команде /search.")

########################################################################Start_search#########################################################################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################

@bot.callback_query_handler(func=lambda call: call.data == '/takekp')
def starting_takekp(message):
	print(message.data)
	have_user=check_contact(message.from_user.id)
	if have_user:
		bot.send_message(message.from_user.id,"Введите информацию которую сейчас у вас запросит бот")
		msg = bot.send_message(message.from_user.id, "Код товара поставщика")
		bot.register_next_step_handler(msg, process_code_step)
	else:
		print ('не зареган')
		print (message.from_user.id)
		bot.send_message(message.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')
		
def process_code_step(message):
    try:
        chat_id = message.from_user.id
        code = message.text
        user_kp = Takekp(code)
        user_kp_dict[chat_id] = user_kp
        msg =  bot.send_message(chat_id, 'Количество товара')
        bot.register_next_step_handler(msg, process_kol_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так')

def process_kol_step(message):
    try:
        chat_id = message.from_user.id
        kol = message.text
        if not kol.isdigit():
            msg =  bot.reply_to(message, 'Количество товара должен состоять из цифр')
            bot.register_next_step_handler(msg, process_kol_step)
            return
        user_kp = user_kp_dict[chat_id]
        user_kp.kol = kol
        msg =  bot.send_message(chat_id, 'Адрес поставки')
        bot.register_next_step_handler(msg, process_address_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так, сообщите @kirosoftware')
def process_address_step(message):
    try:
        chat_id = message.from_user.id
        address = message.text
        user_kp = user_kp_dict[chat_id]
        user_kp.address = address
        msg = bot.send_message(chat_id, 'Дата поставки в формате ГГГГ-ММ-ДД, например: 2018-02-05')
        bot.register_next_step_handler(msg, process_date_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Опаньки что-то пошло не так, сообщите @kirosoftware')
def process_date_step(message):
	try:
		chat_id = message.from_user.id
		date = message.text
		if not validate_date(date):
			msg =  bot.reply_to(message, 'Введите правильную дату в формате ГГГГ-ММ-ДД, например: 2018-02-05')
			bot.register_next_step_handler(msg, process_date_step)
			return
		user_kp = user_kp_dict[chat_id]
		user_kp.date = date
		print (user_kp.code,user_kp.address,user_kp.kol,user_kp.date)
		
		bot.send_message(chat_id,"Ожидайте...")
		leads = {
		"request":  {
		"leads":  {
		"add":  [
		{
		"name":chat_id,
		"status_id":16551064,
		"responsible_user_id":1768789,
		"custom_fields":[
		{
		"id":384517,
		"name":"Адрес поставки",
		"values":[{"value":user_kp.address,"subtype":"1"}]
		},
		{
		"id":384519,
		"name":"Количество",
		"values":[{"value":user_kp.kol}]
		},
		{
		"id":386519,
		"name":"Дата поставки",
		"values":[{"value":user_kp.date}]
		}
		]

		}
		]
		}}}
		set_leads = s.post('https://dbp.amocrm.ru/private/api/v2/json/leads/set',data=json.dumps(leads))
		#print (set_leads.status_code)
		lead_id=(set_leads.json()['response']['leads']['add'][0]["id"])
		print (lead_id)


		##########################SET TOVAR_INFO################################
		request_info="https://dbp.amocrm.ru/contacts/detail/"+str(user_kp.code)
		lead_set_info={
		"request":  {
		"notes":  {
		"add":  [
		{
		"element_id":  lead_id,
		"element_type":  2,
		"note_type":  4,
		"text":  request_info,
		"responsible_user_id": 1768789

		}
		]
		}
		}
		}
		get_contact=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list?query='+str(chat_id))
		contact_id=get_contact.json()['response']['contacts'][0]['id']
		info_to_lead= s.post('https://dbp.amocrm.ru/private/api/v2/json/notes/set',data=json.dumps(lead_set_info))
		print (info_to_lead.status_code)
		#print (info_to_lead.content)

		lead_set_contact={
		"request": {
		"links": {
		"link": [
		{
		"from": "leads",
		"to": "contacts",
		"from_id": lead_id,#lead_id
		"to_id": contact_id #contact_id
		}
		]
		}
		}
		}
		contact_to_lead = s.post('https://dbp.amocrm.ru/private/api/v2/json/links/set',data=json.dumps(lead_set_contact))
		print(contact_to_lead.status_code)
		print(info_to_lead.content)
		bot.send_message(chat_id,"Ваша заявка принята на обработку, логист скоро отправит Контрольное предложение вам на почту\n")
		next_prev_markup = telebot.types.InlineKeyboardMarkup()
		row=[telebot.types.InlineKeyboardButton(u"\U0001F4E3"+" заказать КП",callback_data="/takekp")]
		row2=[telebot.types.InlineKeyboardButton(u"\U0001F4DD"+" Найти аналог",callback_data="/searchsame")]
		row4=[telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Поиск товара",callback_data="/search")]
		next_prev_markup.row(*row)
		next_prev_markup.row(*row2)
		next_prev_markup.row(*row4)

		bot.send_message(message.from_user.id,"Вы в главном меню "+u"\U0001F3AF"+"\n\n" + "* Для поиска продукта нажмите на кнопку \n[ "+u"\U0001F50D"+" Поиск товара ]\n* Для запроса аналога продукта нажмите на кнопку \n[ "+u"\U0001F4DD"+" Найти аналог ]\n * Для запроса КП нажмите на кнопку \n[ "+u"\U0001F4E3"+" заказать КП ]", reply_markup=next_prev_markup)
	except Exception as e:
		print(e)
		bot.reply_to(message, 'Опаньки что-то пошло не так, сообщите @kirosoftware')




@bot.callback_query_handler(func=lambda call: call.data == '/search')
def next(call):
	print(call.data)
	have_user=check_contact(call.from_user.id)
	if have_user:
		msg = bot.send_message(call.from_user.id, "Введите ключевые слова (например марку или модель продукта) что бы найти её в базе поставщиков.")
		bot.register_next_step_handler(msg, process_search_step)
	else:
		print ('Не зареган')
		print (call.from_user.id)
		bot.send_message(call.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')
def process_search_step(message):
	global global_row2
	try:
		chat_id = message.from_user.id
		query_ = message.text
		query = Query(query_)
		query_dict[chat_id] = query
		print(query.query)
		bot.send_message(message.from_user.id,"Идет поиск товара, ожидайте...")
		response=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list/?query='+query.query)# Поиск по контрактам
		print (response.status_code)	
		if len(response.content)==0:
			print("Подобный товар не найден, попробуйте другое ключевое слово или запросите найти данный товар у менеджера")
			next_prev_markup = telebot.types.InlineKeyboardMarkup()			
			row1=[telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Запрос на поиск",callback_data="/searchproduct")]
			row2=[telebot.types.InlineKeyboardButton(u"\U0001F519"+" Назад в меню",callback_data="/back")]
			next_prev_markup.row(*row1)
			next_prev_markup.row(*row2)
			bot.send_message(message.from_user.id,"Подобный товар не найден, попробуйте другое ключевое слово или запросите найти данный товар у менеджера",reply_markup=next_prev_markup)
		else:	
			#print (response.content)
			data = response.json()
			if (data['response']['contacts'][0]['name'].isdigit()) and data['response']['contacts'][0]['custom_fields'][0]['id']=='384511':
				print("Найден юзверь")
				next_prev_markup = telebot.types.InlineKeyboardMarkup()			
				row1=[telebot.types.InlineKeyboardButton(u"\U0001F50D"+" Запрос на поиск",callback_data="/searchproduct")]
				row2=[telebot.types.InlineKeyboardButton(u"\U0001F519"+" Назад в меню",callback_data="/back")]
				next_prev_markup.row(*row1)
				next_prev_markup.row(*row2)
				bot.send_message(message.from_user.id,"Подобный товар не найден, попробуйте другое ключевое слово или запросите найти данный товар у менеджера",reply_markup=next_prev_markup)
			else:
				temp_response=''
				data_count=len(data['response']['contacts'])
				bot.send_message(message.from_user.id,"Найдено товаров: "+str(data_count))
				response=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list/?query='+query.query+'&limit_rows=10&limit_offset=0')# Поиск по контрактам
				if (data_count<10):
					next_prev_markup = telebot.types.InlineKeyboardMarkup()
					row=[]
					row.append(telebot.types.InlineKeyboardButton(u"\u2B05",callback_data="ignore"))
					row.append(telebot.types.InlineKeyboardButton(u"\u27A1",callback_data="ignore"))	
					next_prev_markup.row(*row)
					next_prev_markup.row(*global_row2)
					for i in range(len(data['response']['contacts'])):
						temp_response+=str(i+1)+') '+data['response']['contacts'][i]['name']+'( /'+str(data['response']['contacts'][i]['id'])+' )\n'
					bot.send_message(message.from_user.id,temp_response,reply_markup=next_prev_markup)
				else:
					next_prev_markup = telebot.types.InlineKeyboardMarkup()
					row=[]
					row.append(telebot.types.InlineKeyboardButton(u"\u2B05",callback_data="ignore"))
					row.append(telebot.types.InlineKeyboardButton(u"\u27A1",callback_data="limit_offset:"+str(10)+":"+str(data_count)+":"+query.query))
					next_prev_markup.row(*row)
					next_prev_markup.row(*global_row2)
					for i in range(10):
						temp_response+=str(i+1)+') '+data['response']['contacts'][i]['name']+'( /'+str(data['response']['contacts'][i]['id'])+' )\n'
					bot.send_message(message.from_user.id,temp_response,reply_markup=next_prev_markup)
		############################################################# NEED REPLY_MARKUP /PAY ############################################################################################
		#bot.send_message(message.from_user.id,"Ваша подписка на бота закончилась, чтобы ее продлить оплатите подписку. Что бы это сделать введите /pay")
	except Exception as e:
		print(e)
		bot.send_message(295091909,str(e)+'Search step:')
		#bot.reply_to(message, 'Опаньки, что-то пошло не так. Сообщите @kirosoftware')
########################################################/END_Search#######################################################################################################################

@bot.callback_query_handler(func=lambda call: call.data == '/searchsame')
def searchsame(call):
	print(call.data)
	have_user=check_contact(call.from_user.id)
	if have_user:
		msg = bot.send_message(call.from_user.id, "Введите полную техническую спецификацию продукта ")
		bot.register_next_step_handler(msg, process_searchsame_step)
	else:
		print ('Не зареган')
		print (call.from_user.id)
		bot.send_message(call.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')
def process_searchsame_step(message):
	try:
		leads = {
		"request":  {
		"leads":  {
		"add":  [
		{
		"name":message.from_user.id,
		"status_id":16551067,
		"responsible_user_id":1768789,
		}
		]
		}}}
		set_leads = s.post('https://dbp.amocrm.ru/private/api/v2/json/leads/set',data=json.dumps(leads))
		print (set_leads.status_code)
		lead_id=(set_leads.json()['response']['leads']['add'][0]["id"])
		#print (lead_id)
		analog_info=message.text
		lead_set_info={
					"request":  {
					"notes":  {
					"add":  [
					{
					"element_id":  lead_id,
					"element_type":  2,
					"note_type":  4,
					"text":  analog_info,
					"responsible_user_id": 1768789

					}
					]
					}
					}
					}
		info_to_lead= s.post('https://dbp.amocrm.ru/private/api/v2/json/notes/set',data=json.dumps(lead_set_info))
		print (info_to_lead.status_code)
		#print (info_to_lead.content)
		get_contact=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list?query='+str(message.from_user.id))
		
		contact_id=get_contact.json()['response']['contacts'][0]['id']
		print (contact_id)
		lead_set_contact={
		"request": {
		"links": {
		"link": [
		{
		"from": "leads",
		"to": "contacts",
		"from_id": lead_id,
		"to_id": contact_id
		}
		]
		}
		}
		}
		contact_to_lead = s.post('https://dbp.amocrm.ru/private/api/v2/json/links/set',data=json.dumps(lead_set_contact))
		print(contact_to_lead.status_code)
		print(info_to_lead.content)

		bot.send_message(message.from_user.id, "Запрос на поиск аналога принят в обработку, менеджер передаст наше  предложение по готовности на почту")
		#Запрос на поиск аналога принят в обработку, менеджер передаст наше  предложение по готовности на почту
	except Exception as e:
		#print(e)
		bot.send_message(295091909,str(e)+'Searchsame :')
		bot.reply_to(message, 'Опаньки что-то пошло не так, сообщите @kirosoftware')

#Tovar
@bot.message_handler(content_types=['text']) 
def tovar_info(message):
	have_user=check_contact(message.from_user.id)	
	if have_user:
		if message.text[0]=='/' and message.text[1:].isdigit():
			have_product=False
			have_photo=False
			photo_link=''
			product_info=''
			print (message.text)
			bot.send_message(message.from_user.id,"Ваш запрос принят, ожидайте...")
			response=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list?id='+message.text[1:]+'&type=contact')
			if len(response.content)==0:
				bot.send_message(message.from_user.id,"Данный товар не доступен, сообщение отправлено менеджеру. Просим прощения за неудобства.")
			else:
				data = response.json()
				i=data['response']['contacts'][0]
				product_name="<b>"+i['name']+"</b>\n"
				for j in range(len(i['custom_fields'])):
					#print(i['custom_fields'][j])	
					if i['custom_fields'][j]['id']=='384211': # В наличии если есть
						#print(i['custom_fields'][j]['name'],":\n"+i['custom_fields'][j]['values'][0]['value']) # В наличии
						have_product=True
					if i['custom_fields'][j]['id']=='313569': # Описание товара
						product_info="<b>"+i['custom_fields'][j]['name']+":</b>\n"+i['custom_fields'][j]['values'][0]['value']+'\n\n' # Описание товара(
					if i['custom_fields'][j]['id']=='384187': # Photo
						photo_link=i['custom_fields'][j]['values'][0]['value']+'\n\n'
						#print(photo_link) # Photo
						have_photo=True # Photo

				get_product="<b>Есть в наличии</b>" if have_product else "<b>Нет в наличии</b>"	
				get_photo= photo_link if have_photo else "<b>Нет фотографии</b>\n"
				next_prev_markup = telebot.types.InlineKeyboardMarkup()
				row=[telebot.types.InlineKeyboardButton(u"\U0001F4E3"+" заказать КП",callback_data="/takekp")]
				row2=[telebot.types.InlineKeyboardButton(u"\U0001F4DD"+" Найти аналог",callback_data="/searchsame")]
				row4=[telebot.types.InlineKeyboardButton(u"\U0001F519"+" Назад в меню",callback_data="/back")]
				next_prev_markup.row(*row)
				next_prev_markup.row(*row2)
				next_prev_markup.row(*row4)
				answer_text=product_name+"\n<b>Код товара: "+message.text[1:]+"</b>\n\n"+product_info+get_photo+get_product
				if len(answer_text.encode('utf8'))<4096:
					bot.send_message(message.from_user.id,answer_text,parse_mode='HTML',reply_markup=next_prev_markup)
				else:
					message_count=ceil(len(answer_text)/2000)
					for i in range(message_count):
						if((i+1)*2000)>len(answer_text):
							#print (answer_text[i*1500:(i+1)*2000]+" END!!!")
							bot.send_message(message.from_user.id,answer_text[i*2000:len(answer_text)],parse_mode='HTML',reply_markup=next_prev_markup)
						else:
							if (i+1)*2000==len(answer_text):
								#print (answer_text[i*2000:(i+1)*2000]+" END")
								bot.send_message(message.from_user.id,answer_text[i*2000:(i+1)*2000],parse_mode='HTML',reply_markup=next_prev_markup)
							else:
								if i==0:	
									#print (answer_text[i*2000:(i+1)*2000])
									bot.send_message(message.from_user.id,answer_text[i*2000:(i+1)*2000],parse_mode='HTML')
								else:
									bot.send_message(message.from_user.id,answer_text[i*2000:(i+1)*2000])
							
	else:
		print ('Не зареган')
		#print (message.from_user.id)
		#bot.send_message(message.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')
##########################################################################################################################################################################################################################################################

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def next(call):
	print("Ignore")
	bot.answer_callback_query(call.id, text=u"\U0001F644")

############################################################################################################################################################################################################################################################################################################



@bot.callback_query_handler(func=lambda call: call.data == '/searchproduct')
def searchproduct(call):
	print(call.data)
	have_user=check_contact(call.from_user.id)
	if have_user:
		msg = bot.send_message(call.from_user.id, "Введите полную техническую спецификацию продукта ")
		bot.register_next_step_handler(msg, process_searchproduct_step)
	else:
		print ('Не зареган')
		print (call.from_user.id)
		bot.send_message(call.from_user.id,'Вы не зарегестрированы, нажмите на команду /start')
def process_searchproduct_step(message):
	try:
		leads = {
		"request":  {
		"leads":  {
		"add":  [
		{
		"name":message.from_user.id,
		"status_id":17105347,
		"responsible_user_id":1768789,
		}
		]
		}}}
		set_leads = s.post('https://dbp.amocrm.ru/private/api/v2/json/leads/set',data=json.dumps(leads))
		print (set_leads.status_code)
		lead_id=(set_leads.json()['response']['leads']['add'][0]["id"])
		#print (lead_id)
		analog_info=message.text
		lead_set_info={
					"request":  {
					"notes":  {
					"add":  [
					{
					"element_id":  lead_id,
					"element_type":  2,
					"note_type":  4,
					"text":  analog_info,
					"responsible_user_id": 1768789

					}
					]
					}
					}
					}
		info_to_lead= s.post('https://dbp.amocrm.ru/private/api/v2/json/notes/set',data=json.dumps(lead_set_info))
		print (info_to_lead.status_code)
		#print (info_to_lead.content)
		get_contact=s.get('https://dbp.amocrm.ru/private/api/v2/json/contacts/list?query='+str(message.from_user.id))
		
		contact_id=get_contact.json()['response']['contacts'][0]['id']
		print (contact_id)
		lead_set_contact={
		"request": {
		"links": {
		"link": [
		{
		"from": "leads",
		"to": "contacts",
		"from_id": lead_id,
		"to_id": contact_id
		}
		]
		}
		}
		}
		contact_to_lead = s.post('https://dbp.amocrm.ru/private/api/v2/json/links/set',data=json.dumps(lead_set_contact))
		print(contact_to_lead.status_code)
		print(info_to_lead.content)

		bot.send_message(message.from_user.id, "Запрос на поиск товара принят в обработку, менеджер передаст наше предложение по готовности на почту")
	except Exception as e:
		print(e)
		bot.reply_to(message, 'Опаньки что-то пошло не так, сообщите @kirosoftware')



# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()	
bot.polling(True)
# Set webhook
'''
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)

'''