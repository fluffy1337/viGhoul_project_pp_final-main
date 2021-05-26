import eel
from random import randint
from pprint import pprint

from pairs import pairs
import example as ex
from config import config as CONFIG

PRODUCTION = True

eel.init('wgui')
eel.start('', block=False, size=CONFIG['WIN_SIZE'])

@eel.expose
def WindowClose():
	exit()

lastSentTest = [None]
name, group = '', ''

bikvi = '0123456789ABCDEF'

tokens = CONFIG['TOKENS']
def GenTask(text, base):
	global tokens
	ops = 0
	sTask, sOriginal = '', ''
	for j in range(1, tokens + 1):
		if j % 2 == 0:
			if j < tokens:
				op = '+-*'[randint(0, 1 + int(base <= 4))]
				sTask += f' {op} '
				sOriginal += f' {op} '
		else:
			n = randint(0, 32768)
			sTask += FromDec(n, base)
			sOriginal += str(n)

	t = {}
	t['answer'] = None
	t['text'] = text + f'({base})'
	t['question'] = sTask
	t['correctAnswer'] = FromDec(eval(sOriginal), base)
	return t

@eel.expose
def GetTime():
	return CONFIG['TIME']

@eel.expose
def GenTest(_name, _group, train, typeCount): # генерируем тесты
	global name, group
	name, group = _name, _group
	rs = []
	# for _ in range(CONFIG['T_POSTTOPRE']): #3.1
	# 	rs.append(GenTask(
	# 		'Введите префиксную запись для ',
	# 		lambda stack: PrefixToPostfix(stack[::-1]),
	# 		lambda stack: ' '.join(stack[::-1])
	# 	))
	if train:
		for base, n in typeCount:
			for i in range(n):
				rs.append(GenTask(
					'Вычислите: ',
					base
				))
	else:
		for i in range(CONFIG['NTASKS']):
			rs.append(GenTask(
				'Вычислите: ',
				CONFIG['BASE']
			))
	global lastSentTest
	lastSentTest = []
	for v in rs:
		lastSentTest.append(dict(v))
	if not train:
		for i in range(len(rs)):
			rs[i]['correctAnswer'] = None
	return rs

@eel.expose
def Judge(test, train):
	global lastSentTest
	total = len(lastSentTest)
	done = 0
	tasks = [] # выходная таблица, для GUI (!)
	for i in range(len(lastSentTest)):
		v = lastSentTest[i]
		ok = isinstance(test[i]['answer'], str) and test[i]['answer'].strip().replace(' ', '').upper() == v['correctAnswer'].replace(' ', '') # верность ответа
		lastSentTest[i]['answer'] = test[i]['answer'] # пишем ответ в выход
		if ok:
			done += 1
		tasks.append({
			'answer': test[i]['answer'],
			'correctAnswer': v['correctAnswer'],
			'correct': ok
		})
	mark = done / total
	if not train:
		# print(tasks)
		ex.SendToServer(CONFIG['IP'], name, group, mark, lastSentTest)
	vmark = 0
	for i, threshold in pairs(CONFIG['VRATES']):
		if mark * 100 >= threshold:
			vmark = 5 - i
			break
	return { 'tasks': tasks, 'mark': mark, 'vmark': vmark }

def FromDec(num, to):
	rs = []
	while num > 0:
		rs.append(num % to)
		num //= to
	for i in range(len(rs)):
		rs[i] = bikvi[rs[i]]
	return ''.join(rs[::-1])

def ToDec(num, fr):
	rs = 0
	num = num[::-1]
	for i in range(len(num)):
		p = 0
		for p in range(len(bikvi)):
			if bikvi[p] == num[i]:
				break
		rs += p * (fr ** i)
	return rs

print(ToDec(FromDec(16 ** 4 - 1, 16), 16))

while True:
	eel.sleep(10)