import vk_api 
import olymp
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

#Старт сессии
vk_session = vk_api.VkApi(token = "your token")
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def sender(id: int, text: str, key: str) -> None:
    """
	Присылает сообщение пользователю.
	
	Параметры
	------------------------------------------
	id : идентификатор пользователя vk
	
	text : сообщение пользователю
	
	key : клавиатура передаваемая с сообщением
	------------------------------------------
	"""
    vk.messages.send(user_id = id, message = text, random_id = 0, keyboard = key, dont_parse_links = 1)

def create_key(buts: list) -> str:
	"""
	Создание клавиатуры.
	
	Параметры
	---------------------------------------------------------
	buts : список кнопок 
	---------------------------------------------------------
	Итог выполения : клавиатура для передачи в функциб sender
	---------------------------------------------------------
	"""
	nb = []
	color = ''
	for i in range(len(buts)):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			color = {'green' : 'positive', 'red' : 'negative', 'blue' : 'primary'}[buts[i][k][1]]
			nb[i][k] = {"action": {"type" : "text", "payload" : "{\"button\" : \"" + "1" + "\"}", "label" : f"{text}"}, "color" : f"{color}"}
	first_keyboard = {'one_time' : False, 'buttons' : nb}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii = False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard

def cdate(date1: str) -> int:
	"""
	Сравнение, что дата в формате DD.MM.YYYY
	
	Параметры
	---------------------------------------------------------------------
	date1 : дата для проверки
	---------------------------------------------------------------------
	Итог выполения : 0 - дата не соответствует формату, 1 - соответствует
	---------------------------------------------------------------------
	"""
	if(len(date1) == 10):
		if(date1[2] == "." and date1[5] == "."):
			return 1
	return 0

class User():
	"""
	Класс пользователя в формате id, имя, фамилия, права доступа, текущее состояние, репутация, баланс.
	"""
	def __init__(self, user_id, first_name, second_name, root, mode, rep, balance):
		self.user_id = user_id
		self.first_name = first_name
		self.second_name = second_name
		self.root = root 
		self.mode = mode
		self.rep = rep
		self.balance = balance

#Основные данные
menu = [".olymps", ".profile"]
menu_adm = [".add", ".del", ".all"]
menu_creator = [".add", ".del", ".all", ".user", ".update", ".cash_rep"]
back_key = create_key([[('.back', 'red')]])
start_key = create_key([[(f'{menu[0]}', 'blue'), (f'{menu[1]}', 'green')]])
olymps_key = create_key([[('.math', 'blue'), ('.eco', 'green'), ('.phys', 'red'), ('.prog', 'blue')], [('.other', 'blue'), ('.near', 'blue'), ('.back', 'green')]])
profile_key = create_key([[('.support','green'), ('.back', 'red')]])
reg_key = create_key([[('.reg', 'red')]])
admin_key = create_key([[('.add', 'blue'), ('.del', 'red'), ('.all', 'blue'), ('.save', 'green')], [('.profile', 'blue')]])
gl_admin_key = create_key([[('.add', 'blue'), ('.del', 'red'), ('.all', 'blue'), ('.save', 'green')], [('.profile', 'blue'), ('.update', 'blue')]])
chose_key = create_key([[('.math', 'blue'), ('.eco', 'green'), ('.phys', 'red'), ('.prog', 'blue')], [('.other', 'blue'), ('.back', 'green')]])
rep_bal_key = create_key([[('.rep', 'blue'), ('.balance', 'blue')]])
users = []
olymps = dict()
adds = dict()
updates = dict()

def check(user_id: str) -> int:
	"""
	Проверка прав пользователя
    
	Параметры
	----------------------------------------------------------------------------
	user_id : идентификатор пользователя
	----------------------------------------------------------------------------
	Итог выполения : возвращает уровень прав либо 0, если пользователь не найден
	----------------------------------------------------------------------------
	"""
	if(len(users) == 0):
		return 0
	for user in users:
		if(user.user_id == user_id):
			return user.root
	return 0

def register(user_id: int, first_name: str, second_name: str, root: int = 1, mode: str = "start", rep: int = 0, balance: int = 0) -> None:
	"""
	Регистрация пользователя в формате id, имя, фамилия, права доступа = 1, текущее состояние = start, репутация = 0, баланс = 0
	
	Параметры
	------------------------------------
	user_id : идентификатор пользователя

	first_name : имя пользователя

	second_name : фамилия пользователя

	root : права доступа пользователя

	mode : состояние пользователя

	rep : репутация пользователя

	balance : баланс пользователя
	------------------------------------
	"""
	user = User(user_id, first_name, second_name, root, mode, rep, balance)
	users.append(user)
	return None

def get_name(user_id: int) -> list:
	"""
	Получение имени фамилии пользователя. 
	
	Параметры
	-------------------------------------------
	user_id : идентификатор пользователя
	-------------------------------------------
	Итог выполнения : имя, фамилия пользователя
	-------------------------------------------
	"""
	user_get = vk.users.get(user_ids = (user_id))
	user_get = user_get[0]
	first_name = user_get["first_name"]
	last_name = user_get["last_name"]
	return [first_name, last_name]

def modes(user_id: int, new_mode: str) -> int:
	""" 
	Установление нового текущего состояния для пользователя
	
	Параметры
	-----------------------------------------
	user_id : идентификатор пользователя

	new_mode : новое состояние пользователя
	-----------------------------------------
	Итог выполнения : 1 если успешно, 0 иначе
	-----------------------------------------
	"""
	for i in users:
		if (i.user_id == user_id):
			i.mode = new_mode
			return 1
	return 0

def update_roots(user_id: int, new_root: str) -> int:
	"""
	Изменение прав у пользователя

	Параметры
	-----------------------------------------
	user_id : идентификатор пользователя

	new_root : новые права доступа
	-----------------------------------------
	Итог выполнения : 1 если успешно, 0 иначе
	-----------------------------------------
	"""
	for user in users:
		if(user.user_id == user_id):
			user.root = int(new_root)
			return 1 
	return 0

def get_users() -> None:
	"""
	Получение всех пользователей, при запуске программы из файла.
	"""
	for line in open("users.txt", "r", encoding = "utf-8"):
		line = line.split()
		register(int(line[0]), line[1], line[2], int(line[3]), "start", int(line[5]), int(line[6]))
	return None

def save_olymps(user_id = "none") -> int:
	"""
	Сохрание всех законченных олимпиад в файл. 
	При удачном завершении возвращает 1.
	"""
	f = open("olymps.txt", "a", encoding = "utf-8")
	delete = []
	for name in olymps.keys():
		if(len(olymps[name]) == 5):
			olymp_id = olymp.now_id()
			olymp.new_id()
			f.write(f"{olymp_id} {name} {olymps[name][0]} {olymps[name][1]} {olymps[name][2]} {olymps[name][3]} {olymps[name][4]} \n")
			delete.append(name)
	f.close()
	for i in delete:
		del olymps[i]
	if(user_id != "none"):
		try:
			del adds[user_id]
		except:
			return 0
	return 1

def names_user() -> list:
	"""
	Возвращает имена всех пользователей
	"""
	names = []
	for user in users:
		names.append(user.first_name + " " + user.second_name)
	return names

def update_rep(user_id: int, new_rep: int) -> bool:
	"""
	Изменяет репутацию пользователя  
	
	Параметры
	----------------------------------------------------------
	user_id : идентификатор пользователя

	new_rep : новое значение репутации
	----------------------------------------------------------
	Итог выполнения: true при успешном выполнении, инече false
	"""
	for user in users:
		if(user.user_id == user_id):
			user.rep = new_rep
			return True
	return False

def update_bal(user_id: int, new_bal: int) -> bool:
	"""
	Изменяет баланс пользователя. 
	
	Параметры
	----------------------------------------------------------
	user_id : идентификатор пользователя

	new_bal : новое значение баланса
	----------------------------------------------------------
	Итог выполнения: true при успешном выполнении, инече false
	"""
	for user in users:
		if(user.user_id == user_id):
			user.balance = new_bal
			return True
	return False

def save_user() -> int:
	"""
	Сохрание всех пользователей в файл. При удачном завершении возвращает 1.
	"""
	f = open("users.txt", "w", encoding = "utf-8")
	for user in users:
		f.write(f"{str(user.user_id)} {user.first_name} {user.second_name} {user.root} {user.mode} {user.rep} {user.balance} \n")
	f.close()
	return 1

def profile(user_id: int) -> int:
	"""
	Возвращает всю информацию о пользователе
	
	Параметры
	------------------------------------------
	user_id : идентификатор пользователя
	------------------------------------------
	Итог выполнения: 1 при успешном выполнении
	"""
	for user in users:
		if(user.user_id == user_id):
			return [user.user_id, user.first_name, user.second_name, user.root, user.mode, user.rep, user.balance]
	return 1

def get_mode(user_id: int) -> int:
	"""
	Возвращает текущее состояние пользователя
	
	Параметры
	------------------------------------------
	user_id : идентификатор пользователя
	------------------------------------------
	Итог выполнения: 1 при успешном выполнении
	"""
	for user in users:
		if(user.user_id == user_id):
			return user.mode
	return 1

def answer_new(user_id: int, text: str) -> None:
	"""
	Ответ новому пользователю
	
	Параметры
	------------------------------------
	user_id : идентификатор пользователя

	text : текст пользователя
	------------------------------------
	"""
	if(text == ".reg"):
		name = get_name(user_id)
		register(user_id, name[0], name[1])
		save_user()
		sender(user_id, "Вы зарегистринованы", start_key)
	else:
		sender(user_id, "Нажмите на кнопку для регистрации", reg_key)
	return None

def find_user(name: str) -> int:
	"""
	Поиск человека в базе данных. 
	
	Параметры
	----------------------------------------------------------------------------
	name : имя, фамилия пользователя
	-----------------------------------------------------------------------------
	Итог выполнения: Возвращает -1 если нет пользователя и его user_id, если есть
	"""
	name = name.split()
	for user in users:
		if(user.first_name.lower() == name[0].lower() and user.second_name.lower() == name[1].lower()):
			return user.user_id
	return -1

def answer_user(user_id: int, text: str, mode: str) -> None:
	"""
	Ответ пользователю с уровнем прав 1
	
	Параметры
	-------------------------------------
	user_id : идентификатор пользователя

	text : текст пользователя

	mode : текущее состояние пользователя
	-------------------------------------
	"""
	if(mode == "start"):
		if(text == menu[0]):
			modes(user_id, "olymps")
			sender(user_id, "Меню олимпиад, выберите предмет", olymps_key)
		elif(text == menu[1]):
			modes(user_id, "profile")
			user = profile(user_id)
			mes = f"Имя: {user[1]} {user[2]} \n Баланс: {user[6]} \n Репутация: {user[5]} \n Уровень прав: {user[3]} \n id пользователя: {user[0]}"
			sender(user_id, mes, profile_key)
		else:
			sender(user_id, "Команда не распознана", start_key)
	elif(mode == "profile"):
		if(text == ".support"):
			sender(user_id, "пишите сюда @raykov_dmitry(supporter)", profile_key)
		elif(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", start_key)
		else:
			sender(user_id, "Команда не распознана", profile_key)
	elif(mode == "olymps"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", start_key)
		elif(text == ".near"):
			olympsi = olymp.sel_olymp()
			mes = ""
			for i in olympsi.keys():
				if(int(i) % 10 == 0):
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) +"\n"
					sender(user_id, mes, olymps_key)
					mes = ""
				else:
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) + "\n"
			if(mes != ""):
				sender(user_id, mes, olymps_key)
		elif(text == ".math" or ".eco" or ".phys" or ".prog"):
			olympsi = olymp.sel_olymp()
			mes = ""
			for i in olympsi.keys():
				if(int(i) % 10 == 0):
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) +"\n"
					sender(user_id, mes, olymps_key)
					mes = ""
				else:
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) + "\n"
			if(mes != ""):
				sender(user_id, mes, olymps_key)
		else:
			sender(user_id, "Команда не распознана", olymps_key)
	return None

def answer_admin(user_id: int, text: str, mode: str) -> None:
	"""
	Ответ пользователю с уровнем прав 2
	
	Параметры
	-------------------------------------
	user_id : идентификатор пользователя

	text : текст пользователя

	mode : текущее состояние пользователя
	-------------------------------------
	"""
	if(mode == "start"):
		if(text == ".add"):
			modes(user_id, "name")
			sender(user_id, "Введите название олимпиады", back_key)
		elif(text == ".profile"):
			modes(user_id, "profile")
			user = profile(user_id)
			mes = f"Имя: {user[1]} {user[2]} \n Баланс: {user[6]} \n Репутация: {user[5]} \n Уровень прав: {user[3]} \n id пользователя: {user[0]}"
			sender(user_id, mes, profile_key)
		elif(text == ".del"):
			modes(user_id, "del")
			sender(user_id, "Введите айди олимпиады которую хотите удалить", back_key)
		elif(text == ".all"):
			olympsi = olymp.sel_olymp()
			mes = ""
			for i in olympsi.keys():
				if(int(i) % 10 == 0):
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) +"\n"
					sender(user_id, mes, admin_key)
					mes = ""
				else:
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) + "\n"
			if(mes != ""):
				sender(user_id, mes, admin_key)
		elif(text == ".save"):
			save_user()
			sender(user_id, "Данные об пользователях сохранены", admin_key)
		else:
			sender(user_id, "Команда не распознана", admin_key)
	elif(mode == "name"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			if text not in olymps.keys():
				olymps[text] = []
				sender(user_id, "Введите ссылку на олимпиаду", back_key)
				adds[user_id] = text
				modes(user_id, "url")
			else:
				modes(user_id, "start")
				sender(user_id, "Олимпиаду с таким названием в данный момент вводят или данные поломаны. Обратитесь к @raykov_dmitry(разработчику)", admin_key)
	elif(mode == "del"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:	
			if(olymp.del_olymp(text) == 0):
				modes(user_id, "start")
				sender(user_id, "Олимпиада удалена", admin_key)
			else:
				modes(user_id, "start")
				sender(user_id, "такой олимпиады нету или данные поломаны. Обратитесь к @raykov_dmitry(разработчику)", admin_key)
	elif(mode == "url"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			if(user_id not in adds.keys()):
				modes(user_id, "start")
				sender(user_id, "Ошибка", admin_key)
			else:
				name = adds[user_id]
				if(name not in olymps.keys()):
					modes(user_id, "start")
					sender(user_id, "Ошибка", admin_key)
				else:
					olymps[name].append(text)
					sender(user_id, "Введите дату регистрации в формате DD.MM.YYYY", back_key)
					modes(user_id, "date_reg")
	elif(mode == "date_reg"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			if(cdate(text) == 0):
				sender(user_id, "Неверный формат даты. Введите дату еще раз или вернитесь в стартовое меню.", back_key)
			else:
				name = adds[user_id]
				if(name not in olymps.keys()):
					modes(user_id, "start")
					sender(user_id, "Ошибка", admin_key)
				else:
					olymps[name].append(text)
					sender(user_id, "Введите дату начала в формате DD.MM.YYYY", back_key)
					modes(user_id, "date_start")
	elif(mode == "date_start"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			if(cdate(text) == 0):
				sender(user_id, "Неверный формат даты. Введите дату еще раз или вернитесь в стартовое меню.", back_key)
			else:
				name = adds[user_id]
				if(name not in olymps.keys()):
					modes(user_id, "start")
					sender(user_id, "Ошибка", admin_key)
				else:
					olymps[name].append(text)
					sender(user_id, "Введите уровень олимпиады, если не знаете/нет уровня напишите none", back_key)
					modes(user_id, "olymp_lvl")
	elif(mode == "olymp_lvl"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			name = adds[user_id]
			if(name not in olymps.keys()):
				modes(user_id, "start")
				sender(user_id, "Ошибка", admin_key)
			else:
				olymps[name].append(text)
				sender(user_id, "Выберите предмет олимпиады", chose_key)
				modes(user_id, "chose")
	elif(mode == "chose"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			name = adds[user_id]
			if(name not in olymps.keys()):
				modes(user_id, "start")
				sender(user_id, "Ошибка", admin_key)
			else:
				olymps[name].append(text[1::])
				save_olymps(user_id)
				sender(user_id, "Олимпиада добавлена", admin_key)
				modes(user_id, "start")
	elif(mode == "profile"):
		if(text == ".support"):
			sender(user_id, "пишите сюда @raykov_dmitry(supporter)", profile_key)
		elif(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", admin_key)
		else:
			sender(user_id, "Команда не распознана", profile_key)
	return None

def answer_gl_admin(user_id: int, text: str, mode: str) -> None:
	"""
	Ответ пользователю с уровнем прав 3
	
	Параметры
	-------------------------------------
	user_id : идентификатор пользователя

	text : текст пользователя

	mode : текущее состояние пользователя
	-------------------------------------
	"""
	if(mode == "start"):
		if(text == ".add"):
			modes(user_id, "name")
			sender(user_id, "Введите название олимпиады", back_key)
		elif(text == ".profile"):
			modes(user_id, "profile")
			user = profile(user_id)
			mes = f"Имя: {user[1]} {user[2]} \n Баланс: {user[6]} \n Репутация: {user[5]} \n Уровень прав: {user[3]} \n id пользователя: {user[0]}"
			sender(user_id, mes, profile_key)
		elif(text == ".del"):
			modes(user_id, "del")
			sender(user_id, "Введите айди олимпиады которую хотите удалить", back_key)
		elif(text == ".all"):
			olympsi = olymp.sel_olymp()
			mes = ""
			for i in olympsi.keys():
				if(int(i) % 10 == 0):
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) +"\n"
					sender(user_id, mes, gl_admin_key)
					mes = ""
				else:
					mes += str(i) + ":" + str(olympsi[i][0])+ " - " + str(olympsi[i][1]) + " - " + str(olympsi[i][2]) + " - " + str(olympsi[i][3]) + " - " + str(olympsi[i][4]) + " - " + str(olympsi[i][5]) + "\n"
			if(mes != ""):
				sender(user_id, mes, gl_admin_key)
		elif(text == ".save"):
			save_user()
			sender(user_id, "Данные об пользователях сохранены", gl_admin_key)
		elif(text == ".update"):
			sender(user_id, "Введите Имя Фамилия пользователя", back_key)
			updates[user_id] = ""
			modes(user_id, "update_name")
		else:
			sender(user_id, "Команда не распознана", gl_admin_key)
	elif(mode == "update_name"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			if(find_user(text) == -1):
				sender(user_id, "Человек не найден, повторите попытку", back_key)
			else:
				sender(user_id, "Какой уровень прав будет у человека", back_key)
				modes(user_id, "update_root")
				updates[user_id] = find_user(text)
	elif(mode == "update_root"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			if(text != "1" and text != "2" and text != "3"):
				sender(user_id, "Таких прав нету, введите 1, 2 или 3", back_key)
			else:
				update_roots(updates[user_id], text)
				modes(user_id, "start")
				sender(user_id, " ".join(get_name(updates[user_id])) + "получил права доступа " + text, gl_admin_key)
				save_user()

	elif(mode == "name"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			if text not in olymps.keys():
				olymps[text] = []
				sender(user_id, "Введите ссылку на олимпиаду", back_key)
				adds[user_id] = text
				modes(user_id, "url")
			else:
				modes(user_id, "start")
				sender(user_id, "Олимпиаду с таким названием в данный момент вводят или данные поломаны. Обратитесь к @raykov_dmitry(разработчику)", admin_key)
	elif(mode == "del"):
		if(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:	
			if(olymp.del_olymp(text) == 0):
				modes(user_id, "start")
				sender(user_id, "Олимпиада удалена", gl_admin_key)
			else:
				modes(user_id, "start")
				sender(user_id, "такой олимпиады нету или данные поломаны. Обратитесь к @raykov_dmitry(разработчику)", gl_admin_key)
	elif(mode == "url"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			if(user_id not in adds.keys()):
				modes(user_id, "start")
				sender(user_id, "Ошибка", gl_admin_key)
			else:
				name = adds[user_id]
				if(name not in olymps.keys()):
					modes(user_id, "start")
					sender(user_id, "Ошибка", gl_admin_key)
				else:
					olymps[name].append(text)
					sender(user_id, "Введите дату регистрации в формате DD.MM.YYYY", back_key)
					modes(user_id, "date_reg")
	elif(mode == "date_reg"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			if(cdate(text) == 0):
				sender(user_id, "Неверный формат даты. Введите дату еще раз или вернитесь в стартовое меню.", back_key)
			else:
				name = adds[user_id]
				if(name not in olymps.keys()):
					modes(user_id, "start")
					sender(user_id, "Ошибка", gl_admin_key)
				else:
					olymps[name].append(text)
					sender(user_id, "Введите дату начала в формате DD.MM.YYYY", back_key)
					modes(user_id, "date_start")
	elif(mode == "date_start"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			if(cdate(text) == 0):
				sender(user_id, "Неверный формат даты. Введите дату еще раз или вернитесь в стартовое меню.", back_key)
			else:
				name = adds[user_id]
				if(name not in olymps.keys()):
					modes(user_id, "start")
					sender(user_id, "Ошибка", gl_admin_key)
				else:
					olymps[name].append(text)
					sender(user_id, "Введите уровень олимпиады, если не знаете/нет уровня напишите none", back_key)
					modes(user_id, "olymp_lvl")
	elif(mode == "olymp_lvl"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			name = adds[user_id]
			if(name not in olymps.keys()):
				modes(user_id, "start")
				sender(user_id, "Ошибка", gl_admin_key)
			else:
				olymps[name].append(text)
				sender(user_id, "Выберите предмет олимпиады", chose_key)
				modes(user_id, "chose")
	elif(mode == "chose"):
		if(text == ".back"):
			del olymps[adds[user_id]]
			del adds[user_id]
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			name = adds[user_id]
			if(name not in olymps.keys()):
				modes(user_id, "start")
				sender(user_id, "Ошибка", gl_admin_key)
			else:
				olymps[name].append(text[1::])
				save_olymps(user_id)
				sender(user_id, "Олимпиада добавлена", gl_admin_key)
				modes(user_id, "start")
	elif(mode == "profile"):
		if(text == ".support"):
			sender(user_id, "пишите сюда @raykov_dmitry(supporter)", profile_key)
		elif(text == ".back"):
			modes(user_id, "start")
			sender(user_id, "Вы вернулись в стартовое меню", gl_admin_key)
		else:
			sender(user_id, "Команда не распознана", profile_key)
	return None

# main 
get_users()
while True:
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW:
			if event.to_me:
				textmes = event.text
				user_id = event.user_id
				root = check(user_id)
				mode = get_mode(user_id)
				if(root == 0):
					answer_new(user_id, textmes)
				elif(root == 1):
					answer_user(user_id, textmes, mode)
				elif(root == 2):
					answer_admin(user_id, textmes, mode)
				elif(root == 3):
					answer_gl_admin(user_id, textmes, mode)
