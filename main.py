import sqlite3
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *
from PySide6.QtUiTools import  QUiLoader
from functools import partial
import qdarkstyle



class Contacts(QMainWindow):
    def __init__(self,app ):
        super().__init__()
        self.Result = []
        self.ui =  QUiLoader().load("UI.ui")
        self.ui.show()
        self.conn = sqlite3.connect("Contacts.db")
        self.my_cursor = self.conn.cursor()
        
        self.app=app
        
        self.ui.tableWidget.setColumnCount(5)  
        
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setSortingEnabled(True)  
        ht = ['Name' , 'Family' , 'Mobile' , 'Phone' , 'Email']
        self.ui.tableWidget.setHorizontalHeaderLabels(ht)    
        
        
        self.ui.deletebtn.clicked.connect(partial(self.delete))
        self.ui.deleteAllbtn.clicked.connect(partial(self.deleteAll))
        self.ui.savebtn.clicked.connect(partial(self.create))
        
        self.ui.checkBox.clicked.connect(partial(self.changemode))
        
        
        self.load_data()


    def changemode(self):
        
        if self.ui.checkBox.isChecked():
            self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        else:
            self.app.setStyleSheet(None)

    def load_data(self):
        self.my_cursor.execute("SELECT * FROM Persons")
        self.Result = self.my_cursor.fetchall()  
        self.ui.tableWidget.setRowCount(len(self.Result))
        for i in range(0,len(self.Result)):
            for j in range (1,6):             
                self.ui.tableWidget.setItem(i,j-1, QTableWidgetItem(self.Result[i][j]))      



    def delete(self):
        
        self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow())
        self.my_cursor.execute(f"DELETE FROM Persons WHERE name ='{self.Result[self.ui.tableWidget.currentRow()][1]}';")
        self.conn.commit()
        self.Result.pop(self.ui.tableWidget.currentRow())

    def deleteAll(self):
        self.ui.tableWidget.setRowCount(0)
        self.my_cursor.execute(f"DELETE FROM Persons;")
        self.conn.commit()          
        self.Result = []

    def create(self):

        new_contact = (0,self.ui.name.text(),self.ui.last_name.text(),self.ui.mobile.text(),self.ui.home.text(),self.ui.email.text())
        self.Result.append(new_contact)
        self.my_cursor.execute(f"INSERT INTO Persons (name,family,mobile,home,email)VALUES ('{self.ui.name.text()}', '{self.ui.last_name.text()}', '{self.ui.mobile.text()}','{self.ui.home.text()}','{self.ui.email.text()}');")
        self.conn.commit()
        self.ui.tableWidget.setRowCount(len(self.Result))
        
        for i in range(0,len(self.Result)):
            for j in range (1,6):             
                self.ui.tableWidget.setItem(i,j-1, QTableWidgetItem(self.Result[i][j]))      

        self.ui.name.setText("")
        self.ui.last_name.setText("")
        self.ui.mobile.setText("")
        self.ui.home.setText("")
        self.ui.email.setText("")

            
            
            

app = QApplication()

app.setStyleSheet(qdarkstyle.load_stylesheet())
contacts = Contacts(app)
app.exec()