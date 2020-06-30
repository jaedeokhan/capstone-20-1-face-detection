from tkinter import *
from tkinter import messagebox
import datetime
import cv2
import os
from PIL import Image
import numpy as np
from mtcnn.mtcnn import MTCNN
import sys
import pymysql
# 마지막 페이지로 가는 클래스 포함 패키지
from checkattendance import CheckAttendance
from get_mysql_connect import get_cursor
from exit_class import finish_class

# 153 line
# 175 line
# 191 line 자신의 주소로 설정

date = datetime.datetime.now().date()
date = str(date)

class WebcamPage(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("760x800+0+0")
        self.title('얼굴 인식 출석 시스템 - 데이터 수집 & 웹캠 & 출석 확인')
        self.resizable(False, False)
        # Frame => Top
        self.top = Frame(self, height=200, bg="white")
        self.top.pack(fill=X)

        # Frame => Bottom
        self.bottom = Frame(self, height=600, bg="#326fa8")
        self.bottom.pack(fill=X)

        # Frame => top => headling
        self.heading = Label(self.top, text="얼굴 인식 출석 시스템", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)

        # Frame => top => datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        #===============Login name, passwd Label and Entry======================
        # Frame => bottom => Label, Entry
        self.bottom_title = Label(self.bottom, text='3 : 데이터 학습 & 웹캠 페이지',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=5) 
        
        self.bottom_title = Label(self.bottom, text='첫 번째 데이터 학습을 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=100) 
        
        self.bottom_title = Label(self.bottom, text='두 번째 웹캠 시작을 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=175)
        
        self.bottom_title = Label(self.bottom, text='세 번째 출석 체크확인을 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=250)
        
        train = Button(self.bottom, text='1>데이터 학습', height=4, width=12,
                    font='Sans 12 bold',
                    command=self.train_classifier)
        train.place(x=100, y=400)
        
        webcam = Button(self.bottom, text='2>웹캠 시작!', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.detect_face)
        webcam.place(x=250, y=400)
    
        att = Button(self.bottom, text='3>출석 체크확인', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.go_four)
        att.place(x=400, y=400) 
        
        exit = Button(self.bottom, text='종료', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.iExit)
        exit.place(x=550, y=400) 
        
    def go_four(self):
        people = CheckAttendance()
    
    def detect_face(self):
        # mysql connection 얻어오기
        mydb, mycursor = get_cursor()
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            
            features = None
            features = classifier.detect_faces(img)

            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            coords = []

            for feature in features:
                x, y, w, h = feature['box']
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                id, pred = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int(100 * (1 - pred / 300))
                mydb, mycursor = get_cursor()
                mycursor.execute("SELECT user_name from last_member where id=" + str(id))
                s = mycursor.fetchone()
                s = '' + ''.join(s)
                c_s = s + '님 출석체크를 완료했습니다.'

                if confidence > 80:
                    cv2.putText(img, s + str(confidence) + "%",
                                (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                color,
                                1,
                                cv2.LINE_AA)
                    if confidence >= 85:
                        mycursor.execute("UPDATE last_member SET readcount = readcount + 1 WHERE user_name= '" + s + "'")
                        messagebox.showinfo('Result', c_s)
                        messagebox.showinfo('Result', '종료를 원하시면 Enter를 눌러 주세요.')

                        
                else:
                    cv2.putText(img, "Unknown",
                                (x, y-5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0, 0, 255),
                                1,
                                cv2.LINE_AA)
                
                
                coords = [x, y, w, h]
            return coords
    
        def recognize(img, clf, faceCascade):
            coords = draw_boundary(img,
                                   faceCascade,
                                   1.1, # scaleFactor
                                   10,  # minNeighbors
                                   (255, 255, 255),
                                   "Face",
                                   clf)
            return img

        faceCascade = MTCNN()
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("capstone-20-1-face-detection/classifier.xml")

        video_capture = cv2.VideoCapture(0, cv2.CAP_MSMF)

        while True:
            ret, img = video_capture.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("face detection", img)

            if cv2.waitKey(1) == 13 or 0xFF == ord('q'): 
                break
            
        video_capture.release()
        cv2.destroyAllWindows()
        mydb.commit()
        mydb.close()
        self.bottom_title.focus()
        
    def iExit(self):    
        finish_class(self, self.heading)
        
    def train_classifier(self):
        data_dir = "capstone-20-1-face-detection/final-webcam/final-webcam/data"
        path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L');
            imageNp = np.array(img, 'uint8')
            # user.1.1~200 
            id = int(os.path.split(image)[1].split(".")[1])
            faces.append(imageNp)
            ids.append(id)
        ids = np.array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("capstone-20-1-face-detection/final-webcam/classifier.xml")
        messagebox.showinfo('Result', '데이터 학습을 완료했습니다.')
        self.bottom_title.focus()