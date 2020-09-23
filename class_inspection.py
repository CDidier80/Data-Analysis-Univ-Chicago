from PackageImports import *
import sys

directory_contents = dir()
def addDirectoryToComboBox():
    for i in range(len(directory_contents)):
        dir_element = directory_contents[i]
        print(dir_element)
        print(type(dir_element))
        if i == 10:
            break


# print(QAbstractAnimation.__dict__)

class PyQt5Helper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt5 Package Helper')
        self.setGeometry(50, 50, 1800, 900)
        self.initialize_content()
        self.initialize_interactive_methods()

    def initialize_content(self):
        self.PyQt5ContentList = QTreeView(self)
        model = QStandardItemModel(0, 3)
        model.setHeaderData(0, Qt.Horizontal, "Name")
        model.setHeaderData(1, Qt.Horizontal, "Type")
        model.setHeaderData(2, Qt.Horizontal, "Path")
        self.PyQt5ContentList.setModel(model)
        self.PyQt5ContentList.setGeometry(100, 100, 600, 700)
        for i in range(len(directory_contents)):
            model.insertRow(i)
            model.setData(model.index(i, 0), directory_contents[i])
            model.setData(model.index(i, 1), i)
            model.setData(model.index(i, 2), i)


    def initialize_interactive_methods(self):
        pass

def launch_GUI():
    app_configuration = QApplication(sys.argv)
    application = PyQt5Helper()
    application.show()
    sys.exit(app_configuration.exec_())

launch_GUI()

print(class_inspection.__dict__)