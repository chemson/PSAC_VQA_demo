#界面控制逻辑
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QApplication, QMainWindow,QFileDialog

from PyQt5.QtCore import  pyqtSlot,QUrl,QDir, QFileInfo,Qt,QEvent
from PyQt5.QtGui import QIcon,QKeyEvent,QMouseEvent

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer

from videoqa import Ui_MainWindow
from main_test_frameqa import VideoQA_predict
from  main_test_Action import get_question
from main_test_Action import put_select_ans
from main_test_Action import VideoQA_predict_action
from main_test_Action import predict_the_final_answer
class MainWindow(QtWidgets.QMainWindow):

    #界面初始化
    def __init__(self,parent=None):
        super().__init__(parent)
        #用户选择的文件目录
        self.filename = ""
        #组合窗口
        self.ui=Ui_MainWindow()
        #窗口初始化
        self.ui.setupUi(self)
        #隐藏音量滑动条
        self.ui.volumn_slider.hide()
        # 创建视频播放器
        self.player = QMediaPlayer(self)
        # 信息更新周期, ms
        self.player.setNotifyInterval(1000)
        # 视频显示组件
        self.player.setVideoOutput(self.ui.videoWidget)
        # 事件过滤器
        self.ui.videoWidget.installEventFilter(self)
        #视频总时长
        self.__duration = ""
        #视频当前时长
        self.__curPos = ""
       #信号绑定
        self.__set__signal_respond()

    #信号绑定
    def __set__signal_respond(self):
        #视频播放器初始化
        self.player.stateChanged.connect(self.do_stateChanged)
        #视频播放进度条变化显示
        self.player.positionChanged.connect(self.do_positionChanged)
        #视频进度显示
        self.player.durationChanged.connect(self.do_durationChanged)
        #关闭窗口
        self.ui.closeWindow_btn.clicked.connect(self.do_closeWindow)
        #最小化窗口
        self.ui.hideWindow_btn.clicked.connect(self.do_hideWindow)
        #打开文件按钮
        self.ui.openFile_btn.clicked.connect(self.do_openFile_label_clicked)
        #隐藏左侧提问框
        self.ui.hideLeft_btn.clicked.connect(self.do_hideQuestion)
        self.ui.qa_btn.clicked.connect(self.start_prediction)



        ##  ==============自定义功能函数========================


        ##  ==============event处理函数==========================
    # 预测答案生成
    def start_prediction(self):

        if self.ui.oe_radiobtn.isChecked():
            answer = VideoQA_predict(self.fileName, str(self.ui.question_input.text()))
            self.ui.answer_text.setText(answer)
        else:
            answer = VideoQA_predict_action(self.fileName, str(self.ui.question_input.text()))
            mc_question = ''
            mc_candidate_answer = ''
            self.ui.answer_text.setText(mc_candidate_answer + answer)


    # 窗体关闭时
    def closeEvent(self, event):
        # 窗口关闭时不能自动停止播放，需手动停止
        if (self.player.state() == QMediaPlayer.PlayingState):
            self.player.stop()

    ##事件过滤器
    def eventFilter(self, watched, event):
        if (watched != self.ui.videoWidget):
            return super().eventFilter(watched, event)
        # 鼠标左键按下时，暂停或继续播放
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.player.state() == QMediaPlayer.PlayingState:
                    self.player.pause()
                else:
                    self.player.play()
        return super().eventFilter(watched, event)


        ##  ==========由connectSlotsByName()自动连接的槽函数============
    @pyqtSlot()
    ##播放
    def on_play_btn_clicked(self):
        self.player.play()

    @pyqtSlot()
    ##暂停
    def on_pause_btn_clicked(self):
        self.player.pause()

    @pyqtSlot()
    ##音量按钮
    def on_sound_btn_clicked(self):
        if self.ui.volumn_slider.isVisible():
            self.ui.volumn_slider.hide()
        else:
            self.ui.volumn_slider.show()

    @pyqtSlot(int)
    ##音量调节
    def on_volumn_slider_valueChanged(self, value):
        self.player.setVolume(value)

    @pyqtSlot(int)
    ##播放进度调节
    def on_position_slider_valueChanged(self, value):
        self.player.setPosition(value)

    ##  =============自定义槽函数===============================
    ##状态变化
    def do_stateChanged(self, state):
        isPlaying = (state == QMediaPlayer.PlayingState)
        self.ui.play_btn.setEnabled(not isPlaying)
        self.ui.pause_btn.setEnabled(isPlaying)

    ##文件长度变化
    def do_durationChanged(self, duration):
        self.ui.position_slider.setMaximum(duration)
        secs = duration / 1000  # 秒
        mins = secs / 60  # 分钟
        secs = secs % 60  # 余数秒
        self.__duration = "%d:%d" % (mins, secs)
        if self.__curPos <= self.__duration:
             self.ui.ratio_label.setText(self.__curPos + "/" + self.__duration)
        else:
             self.ui.ratio_label.setText(self.__duration + "/" + self.__duration)

    ##当前播放位置变化
    def do_positionChanged(self, position):
        if (self.ui.position_slider.isSliderDown()):
            return  # 如果正在拖动滑条，退出
        self.ui.position_slider.setSliderPosition(position)
        secs = position / 1000  # 秒
        mins = secs / 60  # 分钟
        secs = secs % 60  # 余数秒
        self.__curPos = "%d:%d" % (mins, secs)
        self.ui.ratio_label.setText(self.__curPos + "/" + self.__duration)

    ##打开文件
    def do_openFile_label_clicked(self):
        # 获取系统当前目录
        curPath = QDir.currentPath()
        #打开文件窗口标题
        title = "选择视频文件"
        #文件过滤器
        filt = "所有文件(*.*)"
        #获取用户选择信息
        self.fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        #如果没有选择文件
        if (self.fileName == ""):
            return
        #获取用户选取的文件信息
        fileInfo = QFileInfo(self.fileName)
        #获取文件路径名
        baseName = fileInfo.fileName()
        #当前播放视频设置为用户选择的视频
        self.ui.currentMedia_label.setText(baseName)
        #获取文件的绝对路径
        curPath = fileInfo.absolutePath()

        # 如果选中多选问题,则获取问题
        if self.ui.mc_radiobtn.isChecked():
            get_ques = get_question(self.fileName)
            get_select = put_select_ans(self.fileName)
            self.ui.question_input.setText(get_ques)
            self.ui.answer_text.setText(get_select)

        # 重设当前目录
        QDir.setCurrent(curPath)
        media = QMediaContent(QUrl.fromLocalFile(self.fileName))
        # 设置播放文件
        self.player.setMedia(media)
        #播放文件
        self.player.play()

    #关闭窗口
    def do_closeWindow(self):
        #获取当前窗口所依赖的载体
        cApp=QApplication.instance()
        #退出载体，关闭窗口
        cApp.quit()

    #最小化窗口
    def do_hideWindow(self):
        self.showMinimized()

    # 隐藏左侧提问框
    def do_hideQuestion(self):
        if self.ui.openFile_btn.isVisible():
            self.ui.openFile_btn.hide()
            self.ui.question_label.hide()
            self.ui.question_input.hide()
            self.ui.qa_btn.hide()
            self.ui.answer_label.hide()
            self.ui.answer_text.hide()
            self.ui.videoWidget.setGeometry(QtCore.QRect(0, 0, self.ui.videoWidget_container.width() +self.ui.videoWidget_container.width()*0.3,self.ui.videoWidget_container.height()+self.ui.videoWidget_container.height()*0))
            self.ui.volumn_slider.setGeometry(
                QtCore.QRect(self.ui.videoWidget_container.width() + self.ui.videoWidget_container.width() * 0.22,
                             self.ui.videoWidget_container.height() - self.ui.videoWidget_container.height() * 0.14, 30,
                             100))
            icon_hideRight = QtGui.QIcon()
            icon_hideRight.addPixmap(QtGui.QPixmap("images/right.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.hideLeft_btn.setIcon(icon_hideRight)
        else:

            self.ui.openFile_btn.show()
            self.ui.question_label.show()
            self.ui.question_input.show()
            self.ui.qa_btn.show()
            self.ui.answer_label.show()
            self.ui.answer_text.show()
            self.ui.videoWidget.setGeometry(QtCore.QRect(0, 0, self.ui.videoWidget_container.width() -self.ui.videoWidget_container.width()*0,self.ui.videoWidget_container.height() + self.ui.videoWidget_container.height()*0))
            self.ui.volumn_slider.setGeometry(
                QtCore.QRect(self.ui.videoWidget_container.width() +self.ui.videoWidget_container.width() * -0.03,
                             self.ui.videoWidget_container.height() +self.ui.videoWidget_container.height() * (-0.14), 30,
                             100))
            icon_hideRight = QtGui.QIcon()
            icon_hideRight.addPixmap(QtGui.QPixmap("images/left.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.hideLeft_btn.setIcon(icon_hideRight)










