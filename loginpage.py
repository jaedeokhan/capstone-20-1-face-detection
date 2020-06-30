from tkinter import *
from tkinter import messagebox
import pymysql
import datetime
# 세 번째 페이지로 가는 클래스 포함 패키지
from webcampage import WebcamPage
from get_mysql_connect import get_cursor
from exit_class import finish_class

date = datetime.datetime.now().date()
date = str(date)

class LoginPage(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.UserId = StringVar()
        self.Userpasswd = StringVar()
        self.geometry("760x800+0+0")
        self.title('얼굴 인식 출석 시스템 - 로그인')
        self.resizable(False, False)
        # frame => top
        self.top = Frame(self, height=200, bg="white")
        self.top.pack(fill=X)
        
        # frame => bottom
        self.bottom = Frame(self, height=600, bg="#326fa8")
        self.bottom.pack(fill=X)
        
        # frame => top => heading
        self.heading = Label(self.top, text="얼굴 인식 출석 시스템", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)
            
        # frame => top => datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        #===============Login name, passwd Label and Entry======================
        # frame => bottom => Label, Entry
        self.bottom_title = Label(self.bottom, text='2 : 로그인 페이지',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=200, y=5) 
        
        self.bottom_title = Label(self.bottom, text='아이디와 비밀번호를 입력해주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=60) 
        #===========================================================================
        #========================2: id, passwd 등등 회원가입========================
        self.idl = Label(self.bottom, text='아이디', font='airal 15 bold')
        self.idl.place(x=100, y=175)
                                                    
        self.idt= Entry(self.bottom, width=55, bd=4, textvariable=self.UserId)
        self.idt.insert(0, "아이디를 입력해주세요.")
        self.idt.place(x=200, y=175)
        self.idt.focus()
        
        self.pdl = Label(self.bottom, text='비밀번호', font='airal 15 bold')
        self.pdl.place(x=100, y=250)
                                                    
        self.pdt= Entry(self.bottom, width=55, bd=4, textvariable=self.Userpasswd)
        self.pdt.insert(0, "비밀번호를 입력해주세요.")
        self.pdt.place(x=200, y=250)      

        btnadd = Button(self.bottom, text='로그인', height=4, width=12,
                        font='Sans 12 bold',
                        command=self.go_three)
        btnadd.place(x=100, y= 400)
        
        btnreset = Button(self.bottom, text='새로고침', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.Reset)
        btnreset.place(x=300, y=400) 
        
        btnexit = Button(self.bottom, text='종료', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.iExit)
        btnexit.place(x=500, y=400) 
    
    def Reset(self):
        self.UserId.set("")
        self.Userpasswd.set("")
        self.idt.focus()
    
    def iExit(self):    
        finish_class(self, self.idt)
        
    def go_three(self):
        if(self.UserId.get()=="아이디를 입력해주세요." or self.Userpasswd.get()=="비밀번호를 입력해주세요."):
            messagebox.showinfo('입력오류', '아이디, 비밀번호 2 가지 모두를 입력해주세요.')
            self.idt.focus()
        else:
            sql = """
                SELECT user_name FROM last_member WHERE user_id=%s AND user_passwd=%s
            """
            val = (self.UserId.get(), self.Userpasswd.get())
            # mysql connection 얻어오기
            mydb, mycursor = get_cursor()
            mycursor.execute(sql, val)
            s = mycursor.fetchone()
            mydb.commit()
            mydb.close()
            if s == None:
                messagebox.showinfo('로그인 실패', '로그인이 실패했습니다.')
                self.UserId.set("")
                self.Userpasswd.set("")
                self.idt.focus()
                
            else:
                s = '' + ''.join(s)
                c_s = str(s) + '님 로그인을 성공했습니다.'
                messagebox.showinfo('로그인 성공', c_s)
                people = WebcamPage()
