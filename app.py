# Import necessary modules from PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox, QListWidget, QDialog, QLineEdit, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QFont, QBrush, QColor
import pandas as pd  # Import pandas for CSV handling
import sys

# Create a dialog for adding a new todo item
class TodoDialog(QDialog):
    def __init__(self, parent=None):
        super(TodoDialog, self).__init__(parent)
        self.setWindowTitle('Add Todo')
        self.todo_edit = QLineEdit()
        # Set Font For the QLineEdit
        font = QFont("arial", 11)
        self.todo_edit.setFont(font)

        self.todo_edit.setFixedHeight(25)
        self.ok_button = QPushButton('Ok')
        self.cancel_button = QPushButton('Cancel')

        layout = QVBoxLayout()
        layout.addWidget(self.todo_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

# Create the main widget for the todo list application
class TodoListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize the user interface
        self.setWindowTitle("Todo List Application")
        self.todo_list = QListWidget()
        # Set Font For the List
        font = QFont("Arial", 11)
        self.todo_list.setFont(font)
        # Define buttons for various actions
        self.add_button = QPushButton('Add')
        self.edit_button = QPushButton('Edit')
        self.delete_button = QPushButton('Delete')
        self.delete_all_button = QPushButton('Delete All')
        self.done_button = QPushButton('Done')
        self.in_progress_button = QPushButton('In Progress')
        self.not_done_button = QPushButton('Not Done')
        self.export_button = QPushButton('Export')
        self.import_button = QPushButton('Import')

        # Layout setup
        layout = QVBoxLayout()
        first_button_layout = QHBoxLayout()
        second_button_layout = QHBoxLayout()

        # Add buttons to layouts
        first_button_layout.addWidget(self.add_button)
        first_button_layout.addWidget(self.edit_button)
        first_button_layout.addWidget(self.delete_button)
        first_button_layout.addWidget(self.delete_all_button)

        second_button_layout.addWidget(self.done_button)
        second_button_layout.addWidget(self.in_progress_button)
        second_button_layout.addWidget(self.not_done_button)
        second_button_layout.addWidget(self.export_button)
        second_button_layout.addWidget(self.import_button)

        # Add layouts to the main layout
        layout.addLayout(first_button_layout)
        layout.addWidget(self.todo_list)
        layout.addLayout(second_button_layout)

        # Connect buttons to their respective functions
        self.add_button.clicked.connect(self.add_todo)
        self.edit_button.clicked.connect(self.edit_todo)
        self.delete_button.clicked.connect(self.delete_todo)
        self.delete_all_button.clicked.connect(self.delete_all)
        self.done_button.clicked.connect(self.done)
        self.in_progress_button.clicked.connect(self.in_progress)
        self.not_done_button.clicked.connect(self.not_done)
        self.export_button.clicked.connect(self.export_items)
        self.import_button.clicked.connect(self.import_items)

        self.setLayout(layout)

    # Function to add a new todo item
    def add_todo(self):
        dialog = TodoDialog()
        if dialog.exec_():
            todo_name = dialog.todo_edit.text()
            if todo_name:
                self.todo_list.addItem(todo_name)

    # Function to edit a todo item
    def edit_todo(self):
        if self.todo_list.currentItem() == None:
            QMessageBox.warning(self, "Error", "You haven't selected any todo to edit")
        current_todo = self.todo_list.currentItem()
        if current_todo:
            dialog = TodoDialog()
            if dialog.exec_():
                edited_todo = dialog.todo_edit.text()
                if edited_todo:
                    current_todo.setText(edited_todo)

    # Function to delete a todo item
    def delete_todo(self):
        if self.todo_list.currentItem() == None:
            QMessageBox.warning(self, "Error", "You haven't selected any todo to delete")
        current_todo = self.todo_list.currentItem()
        if current_todo:
            confirm = QMessageBox.question(self, 'Delete todo', 'Are You Sure You Want To Delete?',
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.todo_list.takeItem(self.todo_list.row(current_todo))

    # Function to delete all todo items
    def delete_all(self):
        if self.todo_list.count() == 0:
            QMessageBox.warning(self, "Error", "You don't have any todo to delete")
            return
        confirm = QMessageBox.question(self, 'Delete All', 'Are You Sure You Want To Delete All Todos? ', QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.todo_list.clear()

    # Function to mark a todo item as done
    def done(self):
        current_todo = self.todo_list.currentItem()
        if current_todo:
            current_todo.setBackground(QBrush(QColor("#8BC34A")))

    # Function to mark a todo item as in progress
    def in_progress(self):
        current_todo = self.todo_list.currentItem()
        if current_todo:
            current_todo.setBackground(QBrush(QColor("#303F9F")))

    # Function to mark a todo item as not done
    def not_done(self):
        current_todo = self.todo_list.currentItem()
        if current_todo:
            current_todo.setBackground(QBrush(QColor("#D32F2F")))

    # Function to export todo items to a CSV file
    def export_items(self):
        if self.todo_list.count() == 0:
            QMessageBox.warning(self, "Error", "You have no item in your list")
        else:
            filename, _ = QFileDialog.getSaveFileName(self, "Export Todos", "", "CSV Files (*.Csv)")
            if filename:
                tasks = []
                for index in range (self.todo_list.count()):
                    item = self.todo_list.item(index)
                    if item.background().color().name() == "#000000":
                        tasks.append({
                            'Task': item.text(),
                            'Color': "#ffffff"
                        })
                    else:
                        tasks.append({
                            'Task': item.text(),
                            'Color': item.background().color().name()
                        })
                df = pd.DataFrame(tasks)
                df.to_csv(filename, index=False)

    # Function to import todo items from a CSV file
    def import_items(self):
        self.todo_list.clear()
        filename, _ = QFileDialog.getOpenFileName(self, "Import Tasks", "", "CSV Files (*.csv)")
        if filename:
            df = pd.read_csv(filename)
            for _, row in df.iterrows():
                item = QListWidgetItem(row['Task'])
                item.setBackground(QColor(row["Color"]))
                self.todo_list.addItem(item)

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    todo_list = TodoListWidget()
    todo_list.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
