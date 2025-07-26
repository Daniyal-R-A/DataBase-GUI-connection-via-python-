from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6 . QtWidgets import QApplication , QDialog , QMainWindow , QMessageBox,QPushButton
import sys

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__()
        # Load the .ui file
        uic.loadUi('Library Management System.ui', self)

        self.setWindowTitle("Library Management System")
        # Show the GUI
        self.show()

        self.issuedOn.setEnabled(0)
        self.issuedBy.setEnabled(0)

        self.comboBox.setCurrentIndex(-1)
        self.comboBox.activated.connect(self.sub_category_handler)
        self.AddButton.clicked.connect(self.handle_add)
        self.checkBox.stateChanged.connect(self.issuance_state)
        self.Okay.clicked.connect(self.verify)
        self.Close.clicked.connect(self.exit)
    
    def exit(self):
        # exit the program
        sys.exit()

    def sub_category_handler(self):
        # subcategory handler according to main category field
        combo_txt = self.comboBox.currentText()
        self.comboBox_2.clear()
        if combo_txt == "Database Systems":
            self.comboBox_2.addItem("ERD")
            self.comboBox_2.addItem("SQL")
            self.comboBox_2.addItem("OLAP")
            self.comboBox_2.addItem("Data Mining")

        elif combo_txt == "OOP":
            self.comboBox_2.addItem("C++")
            self.comboBox_2.addItem("Java")

        elif combo_txt == "Artificial Intelligence":
            self.comboBox_2.addItem("Machine Learning")
            self.comboBox_2.addItem("Robotics")
            self.comboBox_2.addItem("Computer Vision")

    def handle_add(self):
        # author name addition in the list
        name = self.author_name.text()
        self.listWidget.addItem(name)
        self.author_name.clear()

    def issuance_state(self):
        # Enabling/ Disabling issuance fields.
        if self.checkBox.isChecked():
            self.issuedOn.setEnabled(1)
            self.issuedBy.setEnabled(1)
        else:
            self.issuedOn.clear()
            self.issuedBy.clear()
            self.issuedOn.setEnabled(0)
            self.issuedBy.setEnabled(0)
    
    def verify(self):
        # verify on form submission.
        dig = QMessageBox(self)
        dig.setWindowTitle("Message Box")

        # The ISBN should not be more than 12 characters long.
        # The ‘Purchased on’ date must be earlier than today.
        if ( (len(self.ISBN.text()) > 12) | (self.PurchasedOn.date() > QtCore.QDate.currentDate())): 
            dig.setText ("The Length of ISBN is greater than 12 or Purchased On Date is greater than today.")

        # If the book is of the type ‘Journal’ it will have no author.
        elif (self.radioButton_3.isChecked() and self.listWidget.__len__() != 0 ):
            dig.setText ("Book of Journal Type should have no authors.")

        # If the book is not of the type ‘Journal’ it must have atleast one author.
        elif ( not(self.radioButton_3.isChecked()) and self.listWidget.__len__() == 0 ):
            dig.setText ("References books or Text book should have at least one author.")
        
        # If the book is issued to someone, the ‘Issued to’ field must not be empty, and the
        # ‘Issue date’ field must be more than the ‘Purchased On’ field but less than today’s date
        elif (self.checkBox.isChecked()  and ( (len(self.issuedBy.text()) == 0) or (QtCore.QDate.currentDate() < self.issuedOn.date()) or (self.issuedOn.date() < self.PurchasedOn.date())) ):
            dig.setText ("Issued to is empty or Issued Date is not between Purchased On and Today's Date.")
        
        # Else Form is good to go.
        else:            
            dig.setInformativeText ("Book addded successfully!")

        dig.setIcon(QMessageBox.Icon.Information) 
        dig.setStandardButtons (QMessageBox.StandardButton.Ok) 
        dig.exec()
 
app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = UI()  # Create an instance of our class
app.exec()  # Start the application