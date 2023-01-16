# encoding = utf-8

from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog as fd
from win32api import GetMonitorInfo, MonitorFromPoint
import sys, os, script,json

monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
win_width, win_height = work_area[2], work_area[3]
THREADFLAG = 0
tmp_class = ["comman", "manner", "rubbish"]
key_map = ["普通等级","礼貌用语","出口成脏"]
SendKeyRange = ["Enter", ('ctrl', 'Enter')]

class WindowsRoot():
	def __init__(self):
		# 主窗体
		self.root = Tk()
		self.root.title('服务器管理器')
		self.root.geometry('%dx%d+%d+%d'%(win_width // 2, win_height // 2, (win_width - win_width // 2) // 2, (win_height - win_height // 2) // 2))
		self.load_statusbar()
		self.load_menubar()
		self.load_global()
		self.load_entity()
	
	def load_statusbar(self):
		# 状态栏
		self.statusbar = Label(self.root, text="", bd=1, relief=SUNKEN, anchor=W)
		self.statusbar.pack(side=BOTTOM, fill=X)

	def load_menubar(self):
		# 菜单栏
		self.menubar = Menu(self.root, tearoff=False)
		#  ->文件
		self.FileMenu = Menu(self.menubar, tearoff=False)
		self.menubar.add_cascade(label="文件", menu=self.FileMenu)
		self.FileMenu.add_command(label="生成线程", command=self.CreateThread)
		self.FileMenu.add_command(label="删除线程", command=self.DeleteThread)
		self.FileMenu.add_separator()
		self.FileMenu.add_command(label="导出存档", command=self.SaveList)
		self.FileMenu.add_command(label="导入存档", command=self.LoadList)
		#  ->帮助
		self.HelpMenu = Menu(self.menubar, tearoff=False)
		self.menubar.add_cascade(label="帮助", menu=self.HelpMenu)
		self.HelpMenu.add_command(label="关于..", command=None)
		#  ->退出
		self.menubar.add_command(label="退出", command=self.command_exit)
		# 绑定菜单
		self.root.config(menu=self.menubar)

	def load_global(self):
		# 内部变量
		self.SendThreadPool = []
		self.ChooseID = None

	def load_entity(self):
		# 列表框
		self.listbox1 = Listbox(self.root,font=("黑体", 12), borderwidth = 1, relief="sunken")
		self.listbox1.place(relx=0,rely=0,relwidth=0.3,relheight=0.95)
		self.listbox1.bind("<Double-Button-1>", self.getChoose)
		# 信息框
		self.frame1 = Frame(self.root, borderwidth = 1, relief="sunken")
		self.frame1.place(relx=0.3,rely=0,relwidth=0.7,relheight=0.95)		
		self.label1 = Label(self.frame1,font=("黑体", 12), borderwidth = 1, relief="sunken")
		self.label1.place(relx=0,rely=0,relwidth=1,relheight=0.1)
		#
		self.frame2 = Frame(self.frame1, borderwidth = 1, relief="sunken")
		self.frame2.place(relx=0,rely=0.1,relwidth=0.5,relheight=0.8)
		self.ChooseLabel = Label(self.frame2, text="当前选中：",font=("黑体", 16))
		self.ChooseLabel.place(relx=0,rely=0,relwidth=0.5,relheight=0.2)
		self.ChooseShowLabel = Label(self.frame2, text="未选中",font=("黑体", 16, "bold"))
		self.ChooseShowLabel.place(relx=0.5,rely=0,relwidth=0.5,relheight=0.2)
		self.ClassShowLabel = Label(self.frame2, text="未选中",font=("黑体", 12, "bold"))
		self.ClassShowLabel.place(relx=0,rely=0.2,relwidth=1,relheight=0.1)
		self.ClassLevel = StringVar()
		self.ClassLevel.set("脏话程度")
		self.ClassComb = Combobox(self.frame2, textvariable=self.ClassLevel, font=("黑体",12), values=["普通等级","礼貌用语","出口成脏"])
		self.ClassComb.place(relx=0, rely=0.3, relwidth=1, relheight=0.1)
		self.ClassComb.bind("<<ComboboxSelected>>",self.changeClass)
		self.DelayLevel = StringVar()
		self.DelayLevel.set("发送间隔")
		delayRange = [i / 10 for i in range(0,30,2)]
		self.DelayComb = Combobox(self.frame2, textvariable=self.DelayLevel, font=("黑体",12), values=delayRange)
		self.DelayComb.place(relx=0, rely=0.4, relwidth=1, relheight=0.1)
		self.DelayComb.bind("<<ComboboxSelected>>",self.changeDelay)
		self.SendKeyLabel = Label(self.frame2, text="发送按键：未选中",font=("黑体", 12, "bold"))
		self.SendKeyLabel.place(relx=0, rely=0.5, relwidth=1, relheight=0.1)
		self.SendKeyShow = StringVar()
		self.SendKeyShow.set("更改发送按键")
		self.SendKeyComb = Combobox(self.frame2, textvariable=self.SendKeyShow, font=("黑体",12), values=SendKeyRange)
		self.SendKeyComb.place(relx=0, rely=0.6, relwidth=1, relheight=0.1)
		self.SendKeyComb.bind("<<ComboboxSelected>>",self.changeSendKey)
		self.TimesLabel = Label(self.frame2, text="发送次数：未选中",font=("黑体", 12, "bold"))
		self.TimesLabel.place(relx=0, rely=0.7, relwidth=1, relheight=0.1)
		self.TimesLabelDescription = Label(self.frame2, text="数字为发送次数，0与负数、其他为无限循环",font=("黑体", 8))
		self.TimesLabelDescription.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
		self.TimesLabelEntry = Entry(self.frame2,font=("黑体", 16))
		self.TimesLabelEntry.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
		self.TimesLabelEntry.bind("<Return>", self.ChangeCircleTime)
		#
		self.frame3 = Frame(self.frame1, borderwidth = 1, relief="sunken")
		self.frame3.place(relx=0.5,rely=0.1,relwidth=0.5,relheight=0.8)
		self.ThreadInfoLabel = Label(self.frame3, text="Thread Info\n未选中",font=("黑体", 12), borderwidth=3, relief="sunken",anchor=NW)
		self.ThreadInfoLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
		#
		self.frame4 = Frame(self.frame1, borderwidth = 1, relief="sunken")
		self.frame4.place(relx=0,rely=0.9,relwidth=1,relheight=0.1)
		self.prepareDiscriptionLabel = Label(self.frame4, borderwidth = 1, relief="raise", text="准备时间：",font=("黑体", 12))
		self.prepareDiscriptionLabel.place(relx=0,rely=0,relwidth=0.15,relheight=1)
		self.prepareEntry = Entry(self.frame4, borderwidth = 1, relief="raise", text="0",font=("黑体", 16))
		self.prepareEntry.place(relx=0.15,rely=0,relwidth=0.15,relheight=1)
		self.prepareEntry.bind("<Return>", self.ChangePrepareTime)
		self.StartButton = Button(self.frame4, borderwidth = 1, relief="raise", text="启动线程",font=("黑体", 16), command=self.ThreadStart)
		self.StartButton.place(relx=0.3,rely=0,relwidth=0.35,relheight=1)
		self.CloseButton = Button(self.frame4, borderwidth = 1, relief="raise", text="摧毁线程",font=("黑体", 16), command=self.ThreadClose)
		self.CloseButton.place(relx=0.65,rely=0,relwidth=0.35,relheight=1)

	# 自定义函数
	def command_exit(self): # 退出
		self.destroy()

	def ThreadInfoUpgrade(self):
		_string = "Thread Info\n"
		if self.ChooseID != None:
			ChooseThread = self.SendThreadPool[self.ChooseID]
			_string += "id:%d,\nThread_id:%d,\n运行状态:%s,\n脏话程度：%s,\n发送间隔：%s,\n发送按键%s,\n发送次数：%s,\n准备时间：%s,"%(
				ChooseThread.id,
				ChooseThread.id+1,
				str(ChooseThread.isrunning),
				ChooseThread._class,
				str(ChooseThread.delaytime),
				str(ChooseThread.combokey),
				str(ChooseThread._times),
				str(ChooseThread.prepareTime)
				)
		else:
			_string += "未选中"
		self.ThreadInfoLabel.configure(text=_string)

	def getChoose(self, event): # 选中线程
		tmpflag = self.listbox1.curselection()[0]
		ChooseThread = self.SendThreadPool[tmpflag]
		self.StatusShow("线程-%d被选中。"%(ChooseThread.id+1))
		self.label1.configure(text = str(ChooseThread) + " id : " + str(ChooseThread.id))
		self.ChooseID = tmpflag
		self.ChooseShowLabel.configure(text="线程"+str(tmpflag+1))
		self.prepareEntry.delete(0,END)
		self.prepareEntry.insert(END, str(ChooseThread.prepareTime))
		self.ClassShowLabel.configure(text="脏话程度："+key_map[tmp_class.index(ChooseThread._class)])
		self.DelayLevel.set(str(ChooseThread.delaytime))
		self.SendKeyLabel.configure(text="发送按键："+str(ChooseThread.combokey))
		self.TimesLabelEntry.delete(0,END)
		self.TimesLabelEntry.insert(END, str(ChooseThread._times))
		self.ThreadInfoUpgrade()

	def ChangeCircleTime(self, event):
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				try:
					int(self.TimesLabelEntry.get())
				except:
					self.SendThreadPool[self.ChooseID]._times = 0
					self.StatusShow("线程-%d的参数-循环次数 已被修正为%d。"%(self.ChooseID+1, 0))
					self.TimesLabelEntry.delete(0,END)
					self.TimesLabelEntry.insert(END, str(self.SendThreadPool[self.ChooseID]._times))
					return None
				self.SendThreadPool[self.ChooseID]._times = int(self.TimesLabelEntry.get())
				self.StatusShow("线程-%d的参数-循环次数 已被修正为%d。"%(self.ChooseID+1, int(self.TimesLabelEntry.get())))
				self.TimesLabelEntry.delete(0,END)
				self.TimesLabelEntry.insert(END, str(self.SendThreadPool[self.ChooseID]._times))
			else:
				self.StatusShow("线程-%d处于运行状态，禁止修改。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def ChangePrepareTime(self, event):
		try:
			int(self.prepareEntry.get())
		except Exception as e:
			self.StatusShow("请输入数字！单位为秒。")
			return None
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				self.SendThreadPool[self.ChooseID].prepareTime = int(self.prepareEntry.get())
				self.StatusShow("线程-%d的参数-准备时间 已被修正为%s。"%(self.ChooseID+1, self.prepareEntry.get()))
			else:
				self.StatusShow("线程-%d处于运行状态，禁止修改。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def changeClass(self, event):
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				self.SendThreadPool[self.ChooseID]._class = tmp_class[self.ClassComb.current()]
				self.StatusShow("线程-%d的参数-脏话程度 已被修正为%s。"%(self.ChooseID+1, key_map[self.ClassComb.current()]))
				self.ClassShowLabel.configure(text="脏话程度："+key_map[self.ClassComb.current()])
			else:
				self.StatusShow("线程-%d处于运行状态，禁止修改。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def changeDelay(self, event):
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				self.SendThreadPool[self.ChooseID].delaytime = self.DelayComb.current() * 2 / 10
				self.StatusShow("线程-%d的参数-发送间隔 已被修正为%s。"%(self.ChooseID+1 ,str(self.DelayComb.current() * 2 / 10)))
				self.DelayLevel.set(str(self.DelayComb.current() * 2 / 10))
			else:
				self.StatusShow("线程-%d处于运行状态，禁止修改。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def changeSendKey(self, event):
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				self.SendThreadPool[self.ChooseID].combokey = SendKeyRange[self.SendKeyComb.current()]
				self.StatusShow("线程-%d的参数-发送按键 已被修正为%s。"%(self.ChooseID+1 ,str(SendKeyRange[self.SendKeyComb.current()])))
				self.SendKeyLabel.configure(text="发送按键："+str(SendKeyRange[self.SendKeyComb.current()]))
			else:
				self.StatusShow("线程-%d处于运行状态，禁止修改。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def StatusShow(self, _string):
		self.ThreadInfoUpgrade()
		self.statusbar.configure(text=_string)

	def CreateThread(self): # 生成一个线程
		global THREADFLAG
		self.SendThreadPool.append(
			script.SendRubbisnThread(
				_id = THREADFLAG,
				_class = "comman",
				delaytime = 0.1,
				combokey = "Enter",
				_times = 5
				)
			)
		THREADFLAG += 1
		self.UpgradeListBox()

	def DeleteThread(self):
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				tmpflag = self.SendThreadPool[self.ChooseID].id
				self.listbox1.delete(self.ChooseID)
				self.SendThreadPool.pop(self.ChooseID)
				self.ChooseID = None
				self.label1.configure(text = "")
				self.ChooseShowLabel.configure(text="")
				self.prepareEntry.delete(0,END)
				self.ClassShowLabel.configure(text="")
				self.DelayLevel.set("")
				self.SendKeyLabel.configure(text="")
				self.TimesLabelEntry.delete(0,END)
				self.ThreadInfoUpgrade()
				self.StatusShow("线程-%d已删除。"%(tmpflag+1))
			else:
				self.StatusShow("线程-%d处于运行状态。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def SaveList(self):
		filetypes = (
			('json files', '*.json'),
			)
		SaveData = {
		"THREADFLAG" : THREADFLAG,
		"ThreadLIST" : []
		}
		for i in self.SendThreadPool:
			SaveData["ThreadLIST"].append(
				{
				'id' : i.id,
				'_class' : i._class,
				'delaytime' : i.delaytime,
				'combokey' : i.combokey,
				'_times' : i._times,
				'prepareTime' :  i.prepareTime
				}
			)
		open(fd.asksaveasfilename(title = "导出配置",filetypes = filetypes)+".json","w",encoding="utf8").write(json.dumps(SaveData))

	def LoadList(self):
		filetypes = (
			('json files', '*.json'),
			)
		global THREADFLAG
		SaveData = json.loads(open(fd.askopenfilename(title = "导入配置",initialdir = "/",filetypes = filetypes),"r",encoding="utf8").read())
		THREADFLAG = SaveData["THREADFLAG"]
		for i in SaveData["ThreadLIST"]:
			self.SendThreadPool.append(
				script.SendRubbisnThread(
					_id = i['id'],
					_class = i['_class'],
					delaytime = i['delaytime'],
					combokey = i['combokey'],
					_times = i['_times'],
					prepareTime = i['prepareTime']
					)
				)
		self.UpgradeListBox()

	def UpgradeListBox(self):
		self.listbox1.delete(0, END)
		for i in self.SendThreadPool:
			self.listbox1.insert(END, str(i))
			self.listbox1.see(0)

	def ThreadStart(self):
		if self.ChooseID != None:
			if not self.SendThreadPool[self.ChooseID].isrunning:
				self.SendThreadPool[self.ChooseID].start()
				self.StatusShow("线程-%d开始运行。准备时间：%ss"%(self.ChooseID+1, str(self.SendThreadPool[self.ChooseID].prepareTime)))
			else:
				self.StatusShow("线程-%d处于运行状态。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	def ThreadClose(self):
		if self.ChooseID != None:
			if self.SendThreadPool[self.ChooseID].isrunning:
				self.SendThreadPool[self.ChooseID].destroy()
				self.StatusShow("线程-%d结束运行。"%(self.ChooseID+1))
			else:
				self.StatusShow("线程-%d未处于运行状态。"%(self.ChooseID+1))
		else:
			self.StatusShow("线程未被选中。")

	# 主程序函数
	def run(self):
		self.root.mainloop()

	def destroy(self):
		sys.exit()
