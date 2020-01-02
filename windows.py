from PyQt5 import QtWidgets,uic
import sys
import pickle
import os
from models import User,Session,Upload
import pymail
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image
from datetime import datetime
from object_detection import execute
from tagFinder import tagQuery
# from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
from PyQt5.QtCore import QTimer
# from PyQt5.Qt import QApplication, QClipboard
# from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit
# import win32clipboard as clipboard



#####################################################################################
#LOGIN PAGE
#####################################################################################
class LoginScreen(QtWidgets.QMainWindow):

    def __init__(self):
        super(LoginScreen, self).__init__()
        self.do_remember = False
        if os.path.exists('session/rem'):
            with open('session/log','rb') as f:
                user = pickle.load(f)
                self.showHome(user)
        else:
            uic.loadUi(os.path.join('ui','login_screen.ui'), self)
            self.setFixedSize(521, 791)
            
            self.btnLogin=self.findChild(QtWidgets.QPushButton,'btnLogin')
            self.bgImage = self.findChild(QtWidgets.QGraphicsView,'bgImage')
            self.btnViewRegister = self.findChild(QtWidgets.QPushButton,'btnViewRegister')
            self.btnForgot = self.findChild(QtWidgets.QPushButton,'btnForgot')

            self.cbRemember=self.findChild(QtWidgets.QCheckBox,'cbRemember')

            
            self.editEmail=self.findChild(QtWidgets.QLineEdit,'editEmail')
            self.editPass=self.findChild(QtWidgets.QLineEdit,'editPass')
            
            self.labelError = self.findChild(QtWidgets.QLabel,'labelError')
            self.bgImage.setStyleSheet("background-image:url(ui/assets/images/bg.jpg);")

            self.btnLogin.clicked.connect(self.doValidation)

            self.cbRemember.stateChanged.connect(self.remember_me)
            self.btnViewRegister.clicked.connect(self.showNextWindow)
            self.btnForgot.clicked.connect(self.showNextWindow2)
            self.show()

       

    def remember_me(self):
        if self.cbRemember.isChecked():
            self.do_remember=True
        else:
            self.do_remember=False


    def showNextWindow(self):
        self.window = RegisterScreen()
        self.close() 

    def showNextWindow2(self):
        self.window = Forgot_Password_Screen()
        self.close()            

    def doValidation(self):     
        email=self.editEmail.text()
        password= self.editPass.text()
        if len(email) > 11 and '@' in email:        
            ses = Session()
            resultset = ses.query(User).filter(User.email==email).filter(User.password == password).all()
            if len(resultset) == 1:
                self.showHome(user=resultset[0])
            else:
                self.labelError.setText("invalid credentials")
        elif len(email)==0:
            self.labelError.setText("Email Missing")
        else:
            self.labelError.setText("Invalid Email")    

    def showHome(self,user):
        if self.do_remember:
            with open('session/rem','wb') as f:
                pickle.dump('remember=True',f)
        with open('session/log','wb') as f: 
            pickle.dump(user,f)
        self.window = HomeScreen()
        self.close() 


#####################################################################################
#SIGN UP PAGE
#####################################################################################       
class RegisterScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        uic.loadUi(os.path.join('ui','register_screen.ui'), self)
        self.setFixedSize(521, 791)

        self.editName=self.findChild(QtWidgets.QLineEdit,'editName')
        self.editEmail=self.findChild(QtWidgets.QLineEdit,'editEmail')
        self.editPass=self.findChild(QtWidgets.QLineEdit,'editPass')
        self.editCPass=self.findChild(QtWidgets.QLineEdit,'editCPass')
        self.btnRegister=self.findChild(QtWidgets.QPushButton,'btnRegister')
        self.labelError = self.findChild(QtWidgets.QLabel,'labelError')
        self.btnViewLogin=self.findChild(QtWidgets.QPushButton,'btnViewLogin')
        self.bgImage = self.findChild(QtWidgets.QGraphicsView,'bgImage')
        self.bgImage.setStyleSheet("background-image:url(ui/assets/images/bg.jpg);")
        self.btnRegister.clicked.connect(self.doValidation)
        self.btnViewLogin.clicked.connect(self.showNextWindow)
        self.show()

    
    def doValidation(self):
        msg  = self.labelError
        msg.setText('')
        dbses = Session()
        name = self.editName.text()
        print(len(name))
        email = self.editEmail.text()
        password = self.editPass.text()
        cpassword = self.editCPass.text()
        if len(name) > 2 and len(name) <= 50:
            if cpassword == password:
                newUser = User(username=name, email = email, password=password)
                dbses.add(newUser)
                dbses.commit()
                msg.setText('successfully saved, please login to continue')
            else:
                msg.setText('password and confirm password do not match')
        else:
            msg.setText('name should be in range of 3-50 chars ')
    

    
    def showNextWindow(self):
        self.window = LoginScreen()
        self.close()       


#####################################################################################
#FORGOT PASSWORD PAGE
#####################################################################################
class Forgot_Password_Screen(QtWidgets.QMainWindow):
    def __init__(self):
        super(Forgot_Password_Screen, self).__init__()
        uic.loadUi(os.path.join('ui','fp_screen.ui'), self)
        self.setFixedSize(521, 791)
        
        self.editEmail=self.findChild(QtWidgets.QLineEdit,'editEmail')
        self.labelError = self.findChild(QtWidgets.QLabel,'labelError')
        
        self.btnSend_Email=self.findChild(QtWidgets.QPushButton,'btnSend_Email')
        self.btnViewLogin=self.findChild(QtWidgets.QPushButton,'btnViewLogin')
        self.bgImage = self.findChild(QtWidgets.QGraphicsView,'bgImage')
        self.bgImage.setStyleSheet("background-image:url(ui/assets/images/bg.jpg);")
        
        self.btnSend_Email.clicked.connect(self.check)
        self.btnViewLogin.clicked.connect(self.gotBackToLogin)
        self.show()
        
    def check(self):
        email=self.editEmail.text()
        if len(email) > 11 and '@' in email:          
            ses = Session()
            resultset = ses.query(User).filter(User.email==email).all()
            if len(resultset) == 1:
                pymail.send(email)
                self.labelError.setText("Email send")
            else:
                self.labelError.setText("Account doesn't exists")
        elif len(email)==0:
            self.labelError.setText("Email Missing")
        else:
            self.labelError.setText("Invalid Email")   
    
        
        
        
      



    def gotBackToLogin(self):
        self.window = LoginScreen()
        self.close() 

#####################################################################################
#THREAD CLASSES 
#####################################################################################
class ObjectDetectionThread(QThread):
    """
    Runs a counter thread.
    """
    taskCompleted = pyqtSignal(dict)

    def __init__(self,imgpath,parent=None):
        QThread.__init__(self, parent)
        self.imgpath = imgpath

    def run(self):
        results = execute(self.imgpath)
        self.taskCompleted.emit(results)

class ScraperThread(QThread):
    """
    Runs a counter thread.
    """
    taskCompleted = pyqtSignal(list)

    def __init__(self,word,parent=None):
        QThread.__init__(self, parent)
        self.word = word

    def run(self):
        results = tagQuery(self.word)
        self.taskCompleted.emit(results)
#####################################################################################
#HOME PAGE
#####################################################################################
class HomeScreen(QtWidgets.QMainWindow):

    def __init__(self):
        super(HomeScreen, self).__init__()
        uic.loadUi(os.path.join('ui','home_screen.ui'), self)
        self.image_path = None
        self.is_img_uploaded = False
        self.setFixedSize(1400, 800)
        self.results = None

        self.btnBrowse_img=self.findChild(QtWidgets.QPushButton,'btnBrowse_img')
        self.btnClear_img=self.findChild(QtWidgets.QPushButton,'btnClear_img')
        self.btnObj_Detection=self.findChild(QtWidgets.QPushButton,'btnObj_Detection')
        self.btnLogout=self.findChild(QtWidgets.QPushButton,'btnLogout')
        self.btnQuit=self.findChild(QtWidgets.QPushButton,'btnQuit')
        self.btnGet_Tag=self.findChild(QtWidgets.QPushButton,'btnGet_Tag')

        self.label_username=self.findChild(QtWidgets.QLabel,'label_username')
        self.show_img = self.findChild(QtWidgets.QGraphicsView,'show_img')
        self.show_img.setStyleSheet("background-image:url(ui/assets/images/placeholder.jpg) center;")
        self.items_in_img = self.findChild(QtWidgets.QListWidget,'items_in_img')
        self.tag_in_img = self.findChild(QtWidgets.QListWidget,'tag_in_img')
        self.instruction= self.findChild(QtWidgets.QGroupBox,'instructions')
        self.labelUsername=self.findChild(QtWidgets.QLabel,'label_username')
        self.labelMsg=self.findChild(QtWidgets.QLabel,'labelmsg')
        self.bgImage = self.findChild(QtWidgets.QGraphicsView,'bgImage')
        self.listView=self.findChild(QtWidgets.QListWidget,'listWidget')

        self.progressBar=self.findChild(QtWidgets.QProgressBar,'progressBar')
        self.progressBarTags=self.findChild(QtWidgets.QProgressBar,'progressBarTags')

        # hiding the progress bar
        self.progressBar.hide()
        self.progressBarTags.hide()

        self.listView.clicked.connect(self.load_selected_img)
        self.bgImage.setStyleSheet("background-image:url(ui/assets/images/bg.jpg);")
        self.btnLogout.clicked.connect(self.gotBackToLogin)
        self.btnBrowse_img.clicked.connect(self.openFileNameDialog)
        self.btnClear_img.clicked.connect(self.clear_img)
        self.btnObj_Detection.clicked.connect(self.performObjDetection)
        self.btnGet_Tag.clicked.connect(self.get_tag)
        self.load_img_list()
        self.items_in_img.clicked.connect(self.load_selected_tag)
        self.show()

        with open('session/log','rb') as f:
            user = pickle.load(f)     
            self.label_username.setText(user.username)
    
    def load_img_list(self):
        dbses = Session()
        results = dbses.query(Upload).all()
        for pos,imgObj in enumerate(results):
            self.listView.insertItem(pos,imgObj.image)

    def load_selected_img(self,qmodelindex):
        item = self.listView.currentItem()
        path = f'uploads/{item.text()}'
        if os.path.exists(path):
            self.instruction.resize(0,0)
            self.image_path = path
            self.is_img_uploaded = True
            self.items_in_img.clear()
            self.tag_in_img.clear()
            self.labelMsg.setText("")
            self.show_img.setStyleSheet(f"background:url({path}) center no-repeat #fff;")
        else:
            print('image not found')

    def load_selected_tag(self,qmodelindex):
        item = self.items_in_img.currentItem()
        self.tag_in_img.clear()
        data=item.text()
        word=""
        for char in data:
            if char.isdigit()==False and char!='(':     
                word+=char
            else:        
                print(word)
                break
        
        result = tagQuery(word)
        print(result)
        for pos,item, in enumerate(result):
            #self.tag_in_img.insertItem(pos,str(item.get('tag'))+" ("+str(item.get('used'))+")")
            self.tag_in_img.insertItem(pos,str(item[0])+" ("+str(item[1])+")")
        return (result)      

    def get_tag(self):
        self.progressBarTags.show()
        # 1st 5 tags from detect tags in image
        if self.is_img_uploaded:
            if self.results:
                for pos,item, in enumerate(self.results.get('images')):
                    first_5_tag=""
                    print(pos,'----------------',self.results,'==================',type(item))
                    result=(pos,str(item.get('class'))+" ("+str(item.get('score'))+")")
                    print(result)
                    print(type(self.results),self.results)
                    if pos < 5:
                        first_5_tag+=(str(item.get('class'))+" ("+str(item.get('score'))+")")
                        #print(first_5_tag)

                        # showing all tags related to 1st 5 tags in tag collected using scraper
                        word=""
                        for char in first_5_tag:
                            if char.isdigit()==False and char!='(':     
                                word+=char
                            else:        
                                print(word)
                                break
                        scraper = ScraperThread(word, parent=self)
                        scraper.taskCompleted.connect(self.extractScraperData)
                        
                        scraper.start()
                        #print(tags_of_first_5_tag)
            # return (items)                    
        else:
            self.progressBarTags.hide()
            self.labelMsg.setText("1.Please do upload image first\n"+
                                   "2.objection detection,then \n"+
                                   "3.press get insta tag button")

    def extractScraperData(self,tags_of_first_5_tag ):
        for pos,item, in enumerate(tags_of_first_5_tag):
            if pos<5:
                self.tag_in_img.insertItem(pos,str(item[0])+" ("+str(item[1])+")")
        self.progressBarTags.hide()

    def gotBackToLogin(self,user):
        try:os.remove('session/rem')
        except:pass
        try:os.remove('session/log')
        except: pass
        self.window = LoginScreen()
        self.close() 

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","JPG (*.jpg);;JPEG (*.jpeg);;PNG (*.png)", options=options)
        if fileName:
            self.image_path = self.img_resize(fileName)
            print(self.image_path)
            self.show_img.setStyleSheet(f"background:url({self.image_path}) center no-repeat #fff;")
            self.instruction.resize(0,0)
            self.is_img_uploaded = True
        else:
            self.labelMsg.setText("No Image Selected")
            
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
            
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName) 

    def img_resize(self,fileName):
        basewidth = 600
        img = Image.open(fileName)
        w,h = img.size
        if w>h:
            wpercent = (basewidth/float(w))
            hsize = int((float(h)*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.LANCZOS)
        else:
            hpercent=(basewidth/float(h))
            wsize = int((float(w)*float(hpercent)))
            img = img.resize((wsize,basewidth), Image.LANCZOS)

        path = f'uploads/img_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
        print(path)
        img.save(path)

        dbses = Session()
        image = f'img_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
        print(len(image))
        
        if len(image) > 2 and len(image) <= 50:
            newUpload = Upload(image=image)
            dbses.add(newUpload)
            dbses.commit()
        return path

    def clear_img(self):
        self.show_img.setStyleSheet("background-image:url(ui/assets/images/placeholder.jpg) center;") 
        self.instruction.resize(400,180)
        self.labelMsg.setText("")
        self.is_img_uploaded = False
        self.items_in_img.clear()
        self.tag_in_img.clear()
             
    def performObjDetection(self):
        if self.is_img_uploaded:
            self.items_in_img.clear()
            objDetector = ObjectDetectionThread(self.image_path, parent=self)
            objDetector.taskCompleted.connect(self.extractData)
            self.progressBar.show()
            objDetector.start()
        else:
            self.labelMsg.setText("Please upload image first")
    
    def extractData(self,results):
        data = results.get('images')[0].get('classifiers')[0].get('classes')
        print(data)
        # self.items_in_img.setText(results)
        # resultString = "object name".ljust(25)+"score".rjust(10)+"\n"
        # for items in data:
        #     resultString+= str(items.get('class')).ljust(10)+str(round(items.get('score'),2)).rjust(25)+"\n" 
        for pos,item, in enumerate(data):
            self.items_in_img.insertItem(pos,str(item.get('class'))+" ("+str(item.get('score'))+")")
            # result=(pos,str(item.get('class'))+" ("+str(item.get('score'))+")")
        self.progressBar.hide()
        self.results = results