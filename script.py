# encoding : utf-8

import os, json, random, time
import pyperclip, threading
import pyautogui as gui
import inspect, ctypes

rubbishData = json.loads(
	open("rubbishCollect.json","r",encoding="utf8").read()
	)

random.seed(time.time())

class SendRubbisnThread(threading.Thread):
	def __init__(self, _id, _class, delaytime, combokey, _times, prepareTime=3):
		threading.Thread.__init__(self)
		self.daemon = True
		self.id = _id
		self._class = _class # 指定类型
		self.delaytime = delaytime # 延时
		self.combokey  = combokey # 发送组合键
		self._times = _times # 次数，0为无限
		self.prepareTime = prepareTime # 准备时间
		self.isrunning = False # 运行状态

	def run(self):
		self.isrunning = True
		time.sleep(self.prepareTime)
		if self._times > 0:
			for i in range(self._times):
				msg = random.choice(rubbishData[self._class])
				send_msg(msg, self.combokey)
				time.sleep(self.delaytime)
		else:
			while True:
				msg = random.choice(rubbishData[self._class])
				send_msg(msg, self.combokey)
				time.sleep(self.delaytime)

	def destroy(self):
		if self.isrunning:
			_async_raise(self.ident, SystemExit) # 结束进程
			self.isrunning = False

def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")

def send_msg(msg, combokey):
	if len(msg) > 0:
		pyperclip.copy(msg)
		gui.hotkey('ctrl', 'v')
		# combokey = [
		# 'Enter',
		# ('ctrl', 'Enter')
		# ]
		gui.hotkey(combokey)