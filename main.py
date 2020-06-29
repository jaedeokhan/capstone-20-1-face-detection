from tkinter import *
from tkinter import messagebox
import datetime
import random
import time
from mtcnn.mtcnn import MTCNN
import cv2
import pymysql
# 두 번째 페이지로 가는 클래스 포함 패키지
from loginpage import LoginPage
from get_mysql_connect import get_mysql
from exit_class import ExitClass

# 179 line data-dir 자신의 디렉토리 변경

date = datetime.datetime.now().date()
date = str(date)

class Application(object):
    def __init__(self, master):
        self.master = master
        self.UserId = StringVar()
        self.Userpasswd = StringVar()
        self.name = StringVar()
        self.identi = StringVar()
        self.major = StringVar()

        # frame => top
        self.top = Frame(master, height=200, bg="white")
        self.top.pack(fill=X)

        # frame => bottom
        self.bottom = Frame(master, height=600, bg="#326fa8")
        self.bottom.pack(fill=X)

        # frame => top => heading
        self.heading = Label(self.top, text="얼굴 인식 출석 시스템 - 회원가입", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=125, y=75)
            
        # frame => top => datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        #=======================1:회원 가입 페이지 텍스트=======================
        # frame => bottom => Label, Entry 
        self.bottom_title = Label(self.bottom, text='1 : 회원 가입 페이지',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=200, y=5) 
        
        self.bottom_title = Label(self.bottom, text='5가지 항목을 모두 입력해주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=60) 
        #==================================================================
        #========================2: 아이디, 비밀번호, 이름, 학번, 학과 입력 후 회원가입=======
        self.l1 = Label(self.bottom, text='아이디', font='airal 15 bold')
        self.l1.place(x=100, y=135)
                                                    
        self.t1 = Entry(self.bottom, width=60, bd=4, textvariable=self.UserId)
        self.t1.insert(0, "아이디를 입력해주세요.")
        self.t1.place(x=200, y=135)
        self.t1.focus()

        self.l2 = Label(self.bottom, text='비밀번호', font='airal 15 bold')
        self.l2.place(x=100, y=190)
        
        self.t2 = Entry(self.bottom, width=60, bd=5, textvariable=self.Userpasswd)
        self.t2.insert(0, "비밀번호를 입력해주세요.")
        self.t2.place(x=200, y=190)
        
        self.l3 = Label(self.bottom, text='이름', font='airal 15 bold')
        self.l3.place(x=100, y=240)
        
        self.t3 = Entry(self.bottom, width=60, bd=5, textvariable=self.name)
        self.t3.insert(0, "이름을 영문으로 입력해주세요.")
        self.t3.place(x=200, y=240)
    
        self.l4 = Label(self.bottom, text='학번', font='airal 15 bold')
        self.l4.place(x=100, y=290)
        
        self.t4 = Entry(self.bottom, width=60, bd=5, textvariable=self.identi)
        self.t4.insert(0, "학번을 입력해주세요.")
        self.t4.place(x=200, y=290)   
        
        self.l5 = Label(self.bottom, text='학과', font='airal 15 bold')
        self.l5.place(x=100, y=340)
        
        self.t5 = Entry(self.bottom, width=60, bd=5, textvariable=self.major)
        self.t5.insert(0, "학과를 입력해주세요.")
        self.t5.place(x=200, y=340)   
        #====================================================================
        #==============================회원가입, 새로고침, 종료======================
        test = '회원가입\n&\n얼굴 데이터\n수집'
        self.btnSignUp = Button(self.bottom, text=test, height=4,
                               width = 10, font='arial 12 bold',
                               command=self.generate_dataset)
        self.btnSignUp.place(x=100, y=400)
        
        self.btnSignUp = Button(self.bottom, text='로그인\n페이지', height=4,
                               width = 10, font='arial 12 bold',
                               command=self.go_login)
        self.btnSignUp.place(x=250, y=400)
        
        self.btnReset = Button(self.bottom, text="새로고침", height=4,
                                font='arial 12 bold', width=10,
                                command=self.Reset)
        self.btnReset.place(x=400, y=400)
        
        self.btnExit = Button(self.bottom, text='종료', height =4,
                               width = 10, font='arial 12 bold',
                               command=self.iExit)
        self.btnExit.place(x=550, y=400)

    #============로그인 페이지로 바로가기 함수=================
    def go_login(self):
        people = LoginPage()
    #=================================================
    #============새로고침 함수============================
    def Reset(self):
        self.UserId.set("")
        self.Userpasswd.set("")
        self.name.set("")
        self.identi.set("")
        self.major.set("")
        self.t1.focus()
    #=================================================
    #===========종료 함수================================
    def iExit(self):
        ExitClass(self, self.t1)    
    #========회원가입 얼굴 데이터 수집 누르면 실행함수=================
    def generate_dataset(self):
        if(self.t1.get()=="" or self.t1.get() == "아이디를 입력해주세요." or self.t2.get()=="" or self.t3.get()=="" or self.t4.get() =="" or self.t5.get() == ""):
            messagebox.showinfo('입력오류', '아이디, 비밀번호, 이름, 학번, 전공 5 가지 모두를 입력해주세요.')
            self.t1.focus()
        else:
            # mysql connection 얻어오기
            mydb, mycursor = get_mysql()
            mycursor.execute("SELECT * FROM last_member")
            myresult = mycursor.fetchall()
            id = 1
            for x in myresult:
                id += 1
           
            sql = """
               INSERT INTO last_member(id, user_Id, user_passwd, user_name, student_id, student_major) 
               VALUES(%s, %s, %s, %s, %s, %s)
            """
            val = (id, self.t1.get(), self.t2.get(), self.t3.get(), self.t4.get(), self.t5.get())
            mycursor.execute(sql, val)
            mydb.commit()
            mydb.close()
            
            face_classifier = MTCNN()
            def face_cropped(img):
                cropped_face = None
                faces = face_classifier.detect_faces(img)
                if faces is ():
                    return None

                for face in faces:
                    x, y, w, h = face['box']
                    cropped_face = img[y:y+h, x:x+w]

                return cropped_face

            cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
            img_id = 0

            while True:
                ret, frame = cap.read()
                if face_cropped(frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(frame), (200, 200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    data_dir = "capstone-20-1-face-detection/final-webcam"
                    file_name_path = data_dir +"/data/user." + str(id) + "." + str(img_id) + ".jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Cropped face", face)
                    if cv2.waitKey(1) == 13 or int(img_id) == 20:
                        break
                        
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo('Reuslt', '데이터 수집을 성공했습니다.')
            people1 = LoginPage()    
#============Main 페이지========================
def main():
    root = Tk()
    app = Application(root)
    root.title("얼굴 인식 출석 프로그램")
    root.geometry("760x800+0+0")
    root.resizable(False, False)    
    root.mainloop()
#============Start==============================
if __name__ == '__main__':
    main()
    