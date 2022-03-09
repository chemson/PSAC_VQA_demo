#gui程序启动文件
import sys
from PyQt5 import QtWidgets
from videoqa import Ui_MainWindow
from mainWindow import MainWindow
if __name__ == '__main__':
    #实例化一个窗体载体程序
    app = QtWidgets.QApplication(sys.argv)
    #实例化一个窗体
    mainWindow= MainWindow()
    #窗体显示
    mainWindow.show()
    #程序循环启动
    sys.exit(app.exec_())