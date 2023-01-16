# encoding : utf-8

import os, requests, sys, threading
import threading, time, json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
SET_THREAD_NUMBER = 8
SET_FLAG = 0
requests.packages.urllib3.disable_warnings()

def get_url(Catalog, DataFormat, Charset):
	# Catalog in ["common", "qiu", "yang"]
	# DataFormat in ["text", "json", "js"]
	# Charset in ["utf8", "gbk2312"]
	'''
	简单嘴臭,极致享受
	对网友及其亲人的问候语，大约6万条。说脏话，骂人的一言api和调用页面 调用页面 https://act.jiawei.xin:10086/lib/api/index1.php

	魔改特点
	整合了https://github.com/Oohuo/rubbish 和https://github.com/pokemonchw/Dirty 的记录，并且具有如下特性。做了数据分级，有

	做了数据分级，普通等级common，礼貌用语qiu，骂娘等级yang(数量最多)，不加参数默认是common。调用示例 https://act.jiawei.xin:10086/lib/api/maren.php?catalog=yang
	api支持返回纯文本，json，js，不加参数默认返回纯文本。调用示例 https://act.jiawei.xin:10086/lib/api/maren.php?format=json
	api支持返回utf8,或者gbk2312，不加参数默认为utf8。调用示例 https://act.jiawei.xin:10086/lib/api/maren.php?charset=gbk2312
	无数据库，无数据存储，只有三个文件
	qq应用和微信应用内拒绝打开，提示跳转到浏览器
	Github打包下载 git clone https://github.com/xinjiawei/maren.git php7以上
	'''
	return f"https://act.jiawei.xin:10086/lib/api/maren.php?catalog={Catalog}&format={DataFormat}&charset{Charset}"

'''
存储结构：
{
	"comman" : ["", "", ...],
	"manner" : ["", "", ...],
	"rubbish" : ["", "", ...]
}
'''

def SaveData(rawtext, _class, flag):
	rawData = open("rubbishData\\rubbish%d.json"%flag, "r", encoding="utf8").read()
	rawList = json.loads(rawData)
	if rawtext not in rawList[_class]:
		rawList[_class].append(rawtext)
		open("rubbishData\\rubbish%d.json"%flag, "w", encoding="utf8").write(json.dumps(rawList))

def GetRubbish(Catalog, DataFormat, Charset):
	url = get_url(Catalog, DataFormat, Charset)
	response = requests.get(url, headers = headers, verify=False)
	if response.status_code == 200:
		return response.text
	else:
		return False

class GetRubbishThread(threading.Thread):
	def __init__(self, flag, _Catalog, _DataFormat="text", _Charset="utf8"):
		threading.Thread.__init__(self)
		self.daemon = True
		self.flag = flag
		self.getDataNum = 0
		self.Catalog = _Catalog
		self.DataFormat = _DataFormat
		self.Charset = _Charset
		if self.Catalog == "comman":
			self._class = "comman"
		elif self.Catalog == "qiu":
			self._class = "manner"
		else:
			self._class = "rubbish"

	def run(self):
		time.sleep(0.3*self.flag)
		print(str(self.flag)+" is running!")
		while True:
			try:
				rawtext = GetRubbish(self.Catalog, self.DataFormat, self.Charset)
				SaveData(rawtext, self._class, self.flag)
				self.getDataNum += 1
				time.sleep(0.5)
			except Exception as e:
				print(e)

def checkThread(ThreadEntityPool):
	for ThreadEntity in ThreadEntityPool:
		i = str(ThreadEntity.flag)
		j = str(ThreadEntity.getDataNum)
		print(f"线程 - {i} 获取了 {j} 条数据！")
	print("\n")
	
def main():
	rawData = {
		"comman" : [],
		"manner" : [],
		"rubbish" : []
	}
	if not os.path.exists("rubbishData"):
		os.mkdir("rubbishData")
	for i in range(SET_THREAD_NUMBER):
		if not os.path.exists("rubbishData\\rubbish%d.json"%i):
			open("rubbishData\\rubbish%d.json"%i, "w", encoding="utf8").write(json.dumps(rawData))
	ThreadPool = []
	global SET_FLAG
	for i in range(SET_THREAD_NUMBER):
		if i <= 4:
			ThreadPool.append(GetRubbishThread(SET_FLAG, "yang"))
		elif i <= 6:
			ThreadPool.append(GetRubbishThread(SET_FLAG, "comman"))
		else:
			ThreadPool.append(GetRubbishThread(SET_FLAG, "qiu"))
		SET_FLAG += 1
	for i in ThreadPool:
		i.start()
	while True:
		time.sleep(15)
		checkThread(ThreadPool)

if __name__ == '__main__':
	main()