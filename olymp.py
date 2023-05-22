from datetime import date

def today() -> str:
	"""
	Возвращает текущую дату
	"""
	dte = date.today()
	dte = str(dte)
	dte = dte[8:] + "." + dte[5:7] + "." + dte[:4]
	return dte
	
def check_days(date1: str, date2: str) -> int:
	"""
	Возвращает разницу дат в днях

	Параметры
	----------------------------
	date1 : первая дата

	date2 : вторая дата
	----------------------------
	Итог выполнения: кол-во дней
	----------------------------
	"""
	days1 = int(date1[6:]) * 365 + int(date1[3:5]) * 30 + int(date1[:2])
	days2 = int(date2[6:]) * 365 + int(date2[3:5]) * 30 + int(date2[:2])
	return days1 - days2

def clear_file(name: str) -> int:
	"""
	Очищает файл

	Параметры
	------------------------------------
	name : название файла без расширения
	------------------------------------
	"""
	f = open(f'{name}.txt', 'w+', encoding="utf-8")
	f.seek(0)
	f.close()
	return 0

def now_id() -> int:
	"""
	Возвращает последний идентификатор олимпиад
	"""
	f = open("id_olymp.txt", "r", encoding="utf-8")
	now = f.read()
	now = int(now)
	f.close()
	return now

def new_id() -> int:
	"""
	Увеличивает последний идентификатор олимпиад на 1
	"""
	now = now_id()
	clear_file("id_olymp")
	now = int(now)
	f = open("id_olymp.txt", "w", encoding="utf-8")
	now += 1
	f.write(str(now))
	f.close()
	return 0

def check_date(date1: int, date2: int) -> int:
	"""
	Проверяет, что 1 дата позже второй

	Параметры
	-------------------------------------------------------------------------
	date1 : первая дата

	date2 : вторая дата
	-------------------------------------------------------------------------
	Итог выполнения: 1 если первая дата позже, если одинаковые, то 0, иначе 2
	-------------------------------------------------------------------------
	"""
	if(int(date1[6:]) > int(date2[6:])):
		return 1
	elif(int(date1[6:]) < int(date2[6:])):
		return 2
	else:
		if(int(date1[3:5]) > int(date2[3:5])):
			return 1
		elif(int(date1[3:5]) < int(date2[3:5])):
			return 2
		else:
			if(int(date1[:2]) > int(date2[:2])):
				return 1
			elif(int(date1[:2]) < int(date2[:2])):
				return 2
			else:
				return 0

def sel_olymp() -> dict:
	"""
	Возвращает все имеющиеся олимпиады
	"""
	f = open('olymps.txt','r', encoding="utf-8")
	olymp_list = dict()
	for line in f:
		oly = line.split()
		olymp_list[int(oly[0])] = [oly[1], oly[2], oly[3], oly[4], oly[5], oly[6]]
	f.close()
	return olymp_list

def out_oly_near() -> dict:
	"""
	Возвращает олимпиады в ближайшие 7 дней
	"""
	olymp = sel_olymp()
	olymps = dict()
	for i in olymp.keys():
		if(check_date(olymp[i][3], today()) != 2):
			olymps[i] = olymp[i]
	for i in olymps.keys():
		for j in olymps.keys():
			if(check_date(olymps[j][3], olymps[i][3]) == 1):
				temp = olymps[i]
				olymps[i] = olymps[j]
				olymps[j] = temp
	olymp = dict()
	for i in olymps.keys():
		if(check_days(olymps[i][3], today()) <= 7 or check_days(olymps[i][2], today()) <= 7):
			olymp[i] = olymps[i]
		else:
			break
	return olymp

def del_olymp(id_olymp: int) -> int:
	"""
	Удаляет олимпиаду по номеру

	Параметры
	--------------------------
	id_olymp : номер олимпиады 
	--------------------------
	"""
	flag = False
	try:
		id_olymp = int(id_olymp)
	except:
		return 1
	if(int(now_id()) <= id_olymp or int(now_id()) == 1): 
		#Олимпиады не существует или их вообще нету
		return 1
	olymp_list = sel_olymp()
	clear_file("id_olymp.txt")
	clear_file("olymps.txt")
	f = open("id_olymp.txt", "w", encoding="utf-8")
	f.write("1")
	f.close()
	f = open("olymps.txt", "w", encoding="utf-8")
	for i in olymp_list.keys():
		if(int(i) == id_olymp):
			flag = True
			continue
		else:
			if(flag):
				f.write(f"{i - 1} {olymp_list[i][0]} {olymp_list[i][1]} {olymp_list[i][2]} {olymp_list[i][3]} {olymp_list[i][4]} {olymp_list[i][5]} \n")
				new_id()
			else:
				f.write(f"{i} {olymp_list[i][0]} {olymp_list[i][1]} {olymp_list[i][2]} {olymp_list[i][3]} {olymp_list[i][4]} {olymp_list[i][5]} \n")
				new_id()
	f.close()
	return 0

def out_oly_start():
	olymp = sel_olymp()
	olymps = dict()
	for i in olymp.keys():
		if(check_date(olymp[i][3], today()) != 2):
			olymps[i] = olymp[i]
	for i in olymps.keys():
		for j in olymps.keys():
			if(check_date(olymps[j][3], olymps[i][3]) == 1):
				temp = olymps[i]
				olymps[i] = olymps[j]
				olymps[j] = temp
	return olymps

def out_oly_register():
	olymp = sel_olymp()
	olymps = dict()
	for i in olymp.keys():
		if(check_date(olymp[i][2], today()) != 2):
			olymps[i] = olymp[i]
	for i in olymps.keys():
		for j in olymps.keys():
			if(check_date(olymps[j][2], olymps[i][2]) == 1):
				temp = olymps[i]
				olymps[i] = olymps[j]
				olymps[j] = temp
	return olymps
