from PyQt6 import QtWidgets, uic
from PyQt6 . QtWidgets import QDialog , QMessageBox
from PyQt6.QtCore import Qt
import sys

books = [
["0201144719 9780201144710","An introduction to database systems","Database","Reference Book","True"],
["0805301453 9780805301458","Fundamentals of database systems","Database","Reference Book","False"],
["1571690867 9781571690869","Object oriented programming in Java","OOP","Text Book","False"],
["1842652478 9781842652473","Object oriented programming using C++","OOP","Text Book","False"],
["0070522618 9780070522619","Artificial intelligence","AI","Journal","False"],
["0865760047 9780865760042","The Handbook of artificial intelligence","AI","Journal","False"],
]

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        # Load the .ui file
        uic.loadUi('Search_Output.ui', self) 
        
        self.setWindowTitle("Advanced Library Management System")
      
        self.help_print_books()

                
        # Connect the search function with the search button.
        self.Search.clicked.connect(self.search)
        # Connect the view function with the view button.
        self.View.clicked.connect(self.view)
        # Connect the delete function with the delete button.
        self.Delete.clicked.connect(self.delete)
        # Connect the close function with the close button.
        self.Close.clicked.connect(self.close)

    def help_print_books(self): # it is setting the items in books List in booksTableWidget
        self.booksTableWidget.setRowCount(len(books)) 
        for i in range(len(books)):
            for j in range(5):
                item = QtWidgets.QTableWidgetItem(books[i][j])
                # Make the items non-editable
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
                self.booksTableWidget.setItem(i,j,item)
        
    def search(self): # It is searching the element in booksTableWidget based on the search criteria
        combo_txt = self.comboBox.currentText()
        title_txt = self.Title.text()
        issued = self.Issued.isChecked()
        refernce = self.reference.isChecked()
        textbook = self.textbook.isChecked()
        journal = self.journal.isChecked()
        self.booksTableWidget.clearContents()

        if combo_txt or title_txt:
                c = 0; 
                for i in range(len(books)):
                    if (( (books[i][2] == combo_txt) and (title_txt in books[i][1]) and (self.help_issued(issued) == books[i][4]) and (self.help_radio(refernce, textbook, journal) == books[i][3]) )):
                        for j in range(5):   
                            item = QtWidgets.QTableWidgetItem(books[i][j])
                            # Make the items non-editable
                            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
                            self.booksTableWidget.setItem(c,j,item)
                        c += 1
  
        else:
            self.help_print_books()

    def help_issued(self, issued): # returns "True" if the Issued Checkbox is selected 
        if issued == 1: return "True"
        else: return "False"
    
    def help_radio(self, ref, txt, jour): # returns the type of Book, based on radio button selected
        if ref == 1:
            return "Reference Book"
        elif txt == 1:
            return "Text Book"
        elif jour == 1:
            return "Journal"

        
    def view(self): # view the item in seperate window
        
        index = self.booksTableWidget.currentRow()
        if self.booksTableWidget.item(index,0) != None:
            # Get ISBN
            ISBN = self.booksTableWidget.item(index,0).text()
            # Get Title
            Title = self.booksTableWidget.item(index,1).text()
            # Get Category
            Category = self.booksTableWidget.item(index,2).text()
            # Get Type
            Type = self.booksTableWidget.item(index,3).text()
            # Get Issued
            Issued = self.booksTableWidget.item(index,4).text()

            # Pass all the data to view form as parameters
            self.view_form = ViewBook(ISBN,Title,Category,Type,Issued)
            self.view_form.show()

        
    def delete(self): # delete the specified item from books list and redisplay all the items in list.
        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText ("Are you sure you want to delete this book?")
        dig.setIcon(QMessageBox.Icon.Warning) 
        dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            index = self.booksTableWidget.currentRow()
            row_texts = [ # finds the whole text of row in order to search for it in books list.
                self.booksTableWidget.model().index(index, column_index).data()
                for column_index in range(self.booksTableWidget.columnCount())
            ]

            if self.booksTableWidget.item(index,0) != None:
                self.booksTableWidget.clearContents()
                index = books.index(row_texts)
                books.pop(index)
                self.help_print_books()
        
    
    def close(self):
        # exit the program
        sys.exit()
            

class ViewBook(QtWidgets.QMainWindow):  
    def __init__(self,ISBN,Title,Category,Type,Issued):
        super().__init__()

        uic.loadUi('View_Book.ui', self) 

        # Receive Data from the Main Form
        self.ISBN = ISBN
        self.Title = Title
        self.Category = Category
        self.Type = Type
        self.Issued = Issued

        # Set Window Title
        self.setWindowTitle('View Form')

        self.display_isbn.setEnabled(0)
        self.display_title.setEnabled(0)
        self.display_category.setEnabled(0)
        self.display_reference.setEnabled(0)
        self.display_text.setEnabled(0)
        self.display_journal.setEnabled(0)
        self.display_issued.setEnabled(0)

        self.display_reference.setChecked(0)
        self.display_text.setChecked(0)
        self.display_journal.setChecked(0)
        self.display_issued.setChecked(0)

        self.display_isbn.setText(self.ISBN)
        self.display_title.setText(self.Title)
        self.display_category.setText(self.Category)
        if self.Type == "Reference Book":
            self.display_reference.setChecked(1)
        elif self.Type == "Text Book":
            self.display_text.setChecked(1)
        elif self.Type == "Journal":
            self.display_journal.setChecked(1)
        if self.Issued == "True":
            self.display_issued.setChecked(1)

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI() # Create an instance of our 
window.show()
app.exec() # Start the application