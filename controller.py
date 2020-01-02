from windows import LoginScreen
from PyQt5 import QtWidgets, uic
import sys, pickle, os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from models import Base,engine


if __name__ == "__main__":
    
    Base.metadata.create_all(engine)
    app = QtWidgets.QApplication(sys.argv)
    login = LoginScreen()
    app.exec_()