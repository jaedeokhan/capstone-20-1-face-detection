from tkinter import *
from tkinter import messagebox
import datetime
import pymysql
from get_mysql_connect import get_cursor
from exit_class import finish_class

date = datetime.datetime.now().date()
date = str(date)

class CheckAttendance(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("760x800+0+0")
        self.title('데이터 학습, 웹캠')
        self.resizable(False, False)
        # Frame => top
        self.top = Frame(self, height=200, bg="white")
        self.top.pack(fill=X)
        
        # Frame => middle
        self.middle = Frame(self, height=150, bg="#326fa8")
        self.middle.pack(fill=X)
        
        # Frame => bottom 
        self.bottom = Frame(self, height=450, bg="#326fa8")
        self.bottom.pack(fill=X)
        
        # Frame => top => heading
        self.heading = Label(self.top, text="얼굴 인식 출석 시스템", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)
            
        # Frame =>top => datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        # Frame => middle => title
        self.middle_title = Label(self.middle, text='4 : 출석 명단 확인',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.middle_title.place(x=200, y=5) 
        
        # Frame => middle => content
        self.middle_content = Label(self.middle, text='자신의 이름을 확인하고 종료를 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.middle_content.place(x=50, y=100) 

        # Frame => bottom => listbox
        self.scroll = Scrollbar(self.bottom, orient=VERTICAL)
        self.listBox = Listbox(self.bottom, activestyle='underline',
                               width=40, height=27, font='arial 12 bold')
        self.listBox.grid(row=0, column=0, padx=(40, 0))
        self.scroll.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky=N+S)
            
        # mysql connection얻기
        mydb, mycursor = get_cursor()
        mycursor.execute("SELECT * FROM last_member WHERE readcount >= 1 ORDER BY id DESC")
        persons = mycursor.fetchall()
        count = 1
        self.listBox.insert(0, "번호" + "       " + "이름" + "       " + "전공")
        for person in persons:
            self.listBox.insert(count, str(person[0]) + "       " + 
                                str(person[3])  + "       " + str(person[5]))

       # Frame => bottom => button
        btnadd = Button(self.bottom, text="이전 페이지", width=10, height=4,
                       font='arial 12 bold', command=self.previous)
        btnadd.place(x= 550, y = 0)
        
        btnExit = Button(self.bottom, text="종료", width=10, height=4,
                        font='arial 12 bold', command=self.iExit)
        btnExit.place(x=550,  y =  150)

    def previous(self):
        # 세 번째 페이지로 가는 클래스 포함 패키지
        from webcampage import WebcamPage
        people = WebcamPage()
        
    def iExit(self):
        finish_class(self, self.heading)