
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QFileDialog, QStyle, qApp, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QFileInfo
from threading import Timer,Thread,Event
import numpy as np
import time, os, sys, cv2, math, datetime, shutil

screenshots_dir = ("screenshots")
check_folder = os.path.isdir(screenshots_dir)

# If folder doesn't exist, then create it.
if not check_folder:
    os.makedirs(screenshots_dir)
    print("created folder : ", screenshots_dir)
else:
    print(screenshots_dir, "folder already exists.")


class Ui_QtPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = None
        self.isplaying = False
        self.isalternate = False
        self.isScreenshot = False
        self.pathname = None
        self.trimFilename = None
        self.livethread = None
        self.mergeFilename1 = None
        self.mergeFilename2 = None

    def setupUi(self, QtPlayer):

        QtPlayer.setObjectName("QtPlayer")
        QtPlayer.resize(1279, 778)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal,  QtGui.QIcon.On)
        QtPlayer.setWindowIcon(icon)


        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        QtPlayer.setFont(font)
        QtPlayer.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        self.centralwidget = QtWidgets.QWidget(QtPlayer)
        self.centralwidget.setObjectName("centralwidget")


        #merge Ui
        self.mergeFrame = QtWidgets.QFrame(self.centralwidget)
        self.mergeFrame.setGeometry(QtCore.QRect(10, 50, 1261, 711))
        self.mergeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mergeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mergeFrame.setObjectName("mergeFrame")
        self.heading = QtWidgets.QLabel(self.mergeFrame)

        self.heading.setGeometry(QtCore.QRect(510, 50, 221, 91))
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.heading.setFont(font)
        self.heading.setScaledContents(True)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.heading.setObjectName("heading")

        self.file_open1 = QtWidgets.QPushButton(self.mergeFrame)
        self.file_open1.setGeometry(QtCore.QRect(230, 260, 141, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_open1.setFont(font)
        self.file_open1.setObjectName("file_open1")

        self.file_open2 = QtWidgets.QPushButton(self.mergeFrame)
        self.file_open2.setGeometry(QtCore.QRect(860, 260, 141, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_open2.setFont(font)
        self.file_open2.setObjectName("file_open2")

        self.video1select = QtWidgets.QLabel(self.mergeFrame)
        self.video1select.setGeometry(QtCore.QRect(170, 150, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.video1select.setFont(font)
        self.video1select.setAlignment(QtCore.Qt.AlignCenter)
        self.video1select.setObjectName("video1select")

        self.line = QtWidgets.QFrame(self.mergeFrame)
        self.line.setGeometry(QtCore.QRect(610, 190, 20, 171))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.start_merge = QtWidgets.QPushButton(self.mergeFrame)
        self.start_merge.setGeometry(QtCore.QRect(510, 400, 221, 81))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.start_merge.setFont(font)
        self.start_merge.setObjectName("start_merge")

        self.video2select = QtWidgets.QLabel(self.mergeFrame)
        self.video2select.setGeometry(QtCore.QRect(790, 150, 281, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.video2select.setFont(font)
        self.video2select.setAlignment(QtCore.Qt.AlignCenter)
        self.video2select.setObjectName("video2select")

        self.mergeFrame.hide()

        #trimUi

        self.Trimframe = QtWidgets.QFrame(self.centralwidget)
        self.Trimframe.hide()
        self.Trimframe.setGeometry(QtCore.QRect(10, 10, 1261, 711))
        self.Trimframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Trimframe.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Trimframe.setLineWidth(2)
        self.Trimframe.setObjectName("Trimframe")

        self.trimvideo_label = QtWidgets.QLabel(self.Trimframe)
        self.trimvideo_label.setGeometry(QtCore.QRect(0, 0, 1261, 571))
        self.trimvideo_label.setText("")
        self.trimvideo_label.setPixmap(QtGui.QPixmap("Video Trimmer.png"))
        self.trimvideo_label.setScaledContents(True)
        self.trimvideo_label.setObjectName("trimvideo_label")

        self.trimmer_starthorizontalSlider = QtWidgets.QSlider(self.Trimframe)
        self.trimmer_starthorizontalSlider.setGeometry(QtCore.QRect(410, 610, 821, 31))
        self.trimmer_starthorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.trimmer_starthorizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.trimmer_starthorizontalSlider.setTickInterval(0)
        self.trimmer_starthorizontalSlider.setObjectName("trimmer_starthorizontalSlider")

        self.trimVideoSelect = QtWidgets.QPushButton(self.Trimframe)
        self.trimVideoSelect.setGeometry(QtCore.QRect(30, 600, 110, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.trimVideoSelect.setFont(font)
        self.trimVideoSelect.setObjectName("trimVideoSelect")


        self.trimmer_endhorizontalSlider = QtWidgets.QSlider(self.Trimframe)
        self.trimmer_endhorizontalSlider.setGeometry(QtCore.QRect(410, 650, 821, 31))
        self.trimmer_endhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.trimmer_endhorizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.trimmer_endhorizontalSlider.setTickInterval(0)
        self.trimmer_endhorizontalSlider.setObjectName("trimmer_endhorizontalSlider")
        self.trimmer_endhorizontalSlider.sliderPressed.connect(self.endChanged)
        self.trimmer_endhorizontalSlider.sliderReleased.connect(self.endChanged)
        self.trimmer_endhorizontalSlider.valueChanged.connect(self.endChanged)

        self.startTrimming = QtWidgets.QPushButton(self.Trimframe)
        self.startTrimming.setGeometry(QtCore.QRect(30, 650, 120, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.startTrimming.setFont(font)
        self.startTrimming.setObjectName("startTrimming")

        self.selectStartVideo = QtWidgets.QLabel(self.Trimframe)
        self.selectStartVideo.setGeometry(QtCore.QRect(270, 600, 110, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectStartVideo.setFont(font)
        self.selectStartVideo.setObjectName("selectStartVideo")

        self.selectEndVideo = QtWidgets.QLabel(self.Trimframe)
        self.selectEndVideo.setGeometry(QtCore.QRect(270, 650, 110, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectEndVideo.setFont(font)
        self.selectEndVideo.setObjectName("selectEndVideo")
        self.startTrimlabel = QtWidgets.QLabel(self.Trimframe)

        self.startTrimlabel.setGeometry(QtCore.QRect(400, 680, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.startTrimlabel.setFont(font)
        self.startTrimlabel.setObjectName("startTrimlabel")

        self.endTrimlabel = QtWidgets.QLabel(self.Trimframe)
        self.endTrimlabel.setGeometry(QtCore.QRect(1200, 680, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.endTrimlabel.setFont(font)
        self.endTrimlabel.setObjectName("endTrimlabel")
        self.playTrim = QtWidgets.QPushButton(self.Trimframe)
        self.playTrim.setGeometry(QtCore.QRect(170, 625, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.playTrim.setFont(font)
        self.playTrim.setObjectName("playTrim")

        #End trimUi

        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(10, 10, 1261, 571))
        self.video_label.setText("")
        self.video_label.setPixmap(QtGui.QPixmap("background.png"))
        self.video_label.setScaledContents(True)
        self.video_label.setObjectName("video_label")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_label.sizePolicy().hasHeightForWidth())
        self.video_label.setSizePolicy(sizePolicy)

        self.videoPlayerFrame = QtWidgets.QFrame(self.centralwidget)
        self.videoPlayerFrame.setGeometry(QtCore.QRect(10, 600, 1251, 121))
        self.videoPlayerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoPlayerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoPlayerFrame.setObjectName("videoPlayerFrame")


        self.horizontalSlider = QtWidgets.QSlider(self.videoPlayerFrame)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setGeometry(QtCore.QRect(320, 30, 930, 41))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setEnabled(False)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(1)
        self.sliderBusy = False

        self.playButton = QtWidgets.QPushButton(self.videoPlayerFrame)
        self.playButton.setGeometry(QtCore.QRect(0, 30, 75, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.playButton.setFont(font)
        self.playButton.setEnabled(False)
        self.playButton.setObjectName("playButton")

        self.pauseButton = QtWidgets.QPushButton(self.videoPlayerFrame)
        self.pauseButton.setGeometry(QtCore.QRect(90, 30, 75, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pauseButton.setFont(font)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setObjectName("pauseButton")

        self.screenshotButton = QtWidgets.QPushButton(self.videoPlayerFrame)
        self.screenshotButton.setGeometry(QtCore.QRect(0, 80, 165, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.screenshotButton.setFont(font)
        self.screenshotButton.setEnabled(False)
        self.screenshotButton.setObjectName("screenshotButton")

        self.alternateFrames = QtWidgets.QCheckBox(self.videoPlayerFrame)
        self.alternateFrames.setGeometry(QtCore.QRect(170, 30, 161, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.alternateFrames.setEnabled(False)
        self.alternateFrames.setFont(font)
        self.alternateFrames.setObjectName("alternateFrames")

        self.startLabel = QtWidgets.QLabel(self.videoPlayerFrame)
        self.startLabel.setGeometry(QtCore.QRect(315, 80, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(60)
        self.startLabel.setFont(font)
        self.startLabel.setObjectName("startLabel")

        self.endLabel = QtWidgets.QLabel(self.videoPlayerFrame)
        self.endLabel.setGeometry(QtCore.QRect(1190, 70, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(60)
        self.endLabel.setFont(font)
        self.endLabel.setObjectName("endLabel")


        self.liveFrame = QtWidgets.QFrame(self.centralwidget)
        self.liveFrame.setGeometry(QtCore.QRect(10, 600, 1251, 140))
        self.liveFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.liveFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.liveFrame.hide()
        self.liveFrame.setObjectName("liveFrame")

        self.startRecordButton = QtWidgets.QPushButton(self.liveFrame)
        self.startRecordButton.setGeometry(QtCore.QRect(220, 20, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startRecordButton.setFont(font)
        self.startRecordButton.setEnabled(True)
        self.startRecordButton.setObjectName("startRecord")

        self.stopRecordingButton = QtWidgets.QPushButton(self.liveFrame)
        self.stopRecordingButton.setGeometry(QtCore.QRect(500, 20, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.stopRecordingButton.setFont(font)
        self.stopRecordingButton.setEnabled(False)
        self.stopRecordingButton.setObjectName("stopRecordingButton")

        self.liveFeedFolder = QtWidgets.QPushButton(self.liveFrame)
        self.liveFeedFolder.setGeometry(QtCore.QRect(780, 20, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.liveFeedFolder.setFont(font)
        self.liveFeedFolder.setObjectName("liveFeedFolder")


        QtPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QtPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1279, 26))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        QtPlayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QtPlayer)
        self.statusbar.setObjectName("statusbar")
        QtPlayer.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(QtPlayer)
        self.actionOpen.setObjectName("actionOpen")
        self.actionRename = QtWidgets.QAction(QtPlayer)
        self.actionRename.setObjectName("actionRename")
        self.actionVideo_Info = QtWidgets.QAction(QtPlayer)
        self.actionVideo_Info.setEnabled(False)
        self.actionVideo_Info.setObjectName("actionVideo_Info")
        self.actionVideoPlayer = QtWidgets.QAction(QtPlayer)
        self.actionVideoPlayer.setObjectName("actionVideoPlayer")
        self.actionVideoPlayer.setEnabled(True)
        self.actionLiveFeed = QtWidgets.QAction(QtPlayer)
        self.actionLiveFeed .setObjectName("actionLiveFeed")
        self.actionExit_Player = QtWidgets.QAction(QtPlayer)
        self.actionExit_Player.setObjectName("actionExit_Player")
        self.actionTrim = QtWidgets.QAction(QtPlayer)
        self.actionTrim.setObjectName("actionTrim")
        self.actionMerge = QtWidgets.QAction(QtPlayer)
        self.actionMerge.setObjectName("actionMerge")
        self.actionSave_Frames = QtWidgets.QAction(QtPlayer)
        self.actionSave_Frames.setObjectName("actionSave_Frames")
        self.actionSave_Frames.setEnabled(False)
        self.menuMenu.addAction(self.actionOpen)
        self.menuMenu.addAction(self.actionRename)
        self.menuMenu.addAction(self.actionVideo_Info)
        self.menuMenu.addAction(self.actionVideoPlayer)
        self.menuMenu.addAction(self.actionLiveFeed)
        self.menuMenu.addAction(self.actionExit_Player)
        self.menuEdit.addAction(self.actionTrim)
        self.menuEdit.addAction(self.actionMerge)
        self.menuEdit.addAction(self.actionSave_Frames)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        #all connections
        self.actionLiveFeed.triggered.connect(lambda: self.onLiveFeedMode())
        self.actionVideoPlayer.triggered.connect(lambda: self.onVideoPlayerMode())
        self.actionRename.triggered.connect(lambda: self.onRename())
        self.actionVideo_Info.triggered.connect(lambda: self.show_file_info())
        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionExit_Player.triggered.connect(lambda: self.on_exit())
        self.actionSave_Frames.triggered.connect(lambda: self.onSaveFrames())
        self.pauseButton.clicked.connect(lambda : self.onchange())
        self.screenshotButton.clicked.connect(lambda: self.onScreenshot())
        self.playButton.clicked.connect(lambda: self.onchange())
        self.alternateFrames.stateChanged.connect(lambda: self.onAlternate())
        self.startRecordButton.clicked.connect(lambda: self.onStartRecord())
        self.stopRecordingButton.clicked.connect(lambda: self.onStopRecord())
        self.liveFeedFolder.clicked.connect(lambda: self.onLiveFeedFolder())
        self.trimmer_starthorizontalSlider.sliderPressed.connect(self.startChanged)
        self.trimmer_starthorizontalSlider.sliderReleased.connect(self.startChanged)
        self.trimmer_starthorizontalSlider.valueChanged.connect(self.startChanged)
        self.horizontalSlider.sliderPressed.connect(self.horizontalSliderPressed)
        self.horizontalSlider.sliderReleased.connect(self.horizontalSliderReleased)
        self.horizontalSlider.valueChanged.connect(self.sliderValueChanged)
        self.actionTrim.triggered.connect(lambda: self.onTrimSelect())
        self.trimVideoSelect.clicked.connect(lambda: self.onSelectTrimVideo())
        self.playTrim.clicked.connect(lambda: self.onPlay())
        self.startTrimming.clicked.connect(lambda : self.onStartTrim())
        self.actionMerge.triggered.connect(lambda: self.onMerge())
        self.file_open1.clicked.connect(lambda: self.onVideo1Select())
        self.file_open2.clicked.connect(lambda: self.onVideo2Select())
        self.start_merge.clicked.connect(lambda: self.onStartMerge())

        self.retranslateUi(QtPlayer)
        QtCore.QMetaObject.connectSlotsByName(QtPlayer)




#all merge functions
    def onMerge(self):
        self.Trimframe.hide()
        self.video_label.hide()
        self.videoPlayerFrame.hide()
        self.mergeFrame.show()
        self.actionOpen.setEnabled(False)
        self.start_merge.setEnabled(False)

    def onVideo1Select(self):
        try:
            self.mergeFilename1, _ = QFileDialog.getOpenFileName(self, "Open Video to Merge",directory=QtCore.QDir.currentPath())
            self.video1select.setText("Video1 Selected")
            self.enableMerge()
        except:
            self.onError("SomeError Occured")

    def onVideo2Select(self):
        try:
            self.mergeFilename2, _ = QFileDialog.getOpenFileName(self, "Open Video to Merge",directory=QtCore.QDir.currentPath())
            self.video2select.setText("Video2 Selected")
            self.enableMerge()
        except:
            self.onError("SomeError Occured")

    def enableMerge(self):
        if self.mergeFilename2 is not None and self.mergeFilename2 is not None:
            self.start_merge.setEnabled(True)

    def onMergeComplete(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Merging Successful")
        msg.exec_()

    def onStartMerge(self):
        cap = cv2.VideoCapture(self.mergeFilename1)
        # cap1 = cv2.VideoCapture(self.mergeFilename2)
        ret, frame = cap.read()
        i = 1
        # ret1, frame1 = cap1.read()
        out = cv2.VideoWriter('Mergeoutput.avi', cv2.VideoWriter_fourcc(*'XVID'), cap.get(cv2.CAP_PROP_FPS), (frame.shape[1],frame.shape[0]))
        while(cap.isOpened()):
        #     ret, frame = cap.read()
        #     ret1, frame1 = cap1.read()
        #     if ret and ret1: 
        #         h,w,c = frame.shape;
        #         h1,w1,c1 = frame1.shape;
        #         if h != h1 or w != w1: # resize right img to left size
        #             frame1 = cv2.resize(frame1,(w,h))
        #         both = np.concatenate((frame, frame1), axis=1)
        #         out.write(both)
        #     else: 
        #         break
        # while(cap.isOpened()):
            ret, frame = cap.read()
            if frame is None:
                if i>=2:
                    break
                i+=1
                print ("end of video " +  " 2nd.. next one now")
                if i == 2:
                    cap = cv2.VideoCapture(self.mergeFilename2)
                ret, frame = cap.read()
            out.write(frame)

        cap.release()
        out.release()
        self.onMergeComplete()


#end of merge functions





#Trim related Functions

    def onTrimSelect(self):
        if isinstance(self.livethread, LiveVideoThread):
            self.livethread.isLive = False
        self.liveFrame.hide()
        self.actionVideoPlayer.setEnabled(True)
        self.video_label.hide()
        self.videoPlayerFrame.hide()
        self.Trimframe.show()
        self.Trimframe.setEnabled(True)
        self.trimmer_endhorizontalSlider.setEnabled(False)
        self.trimmer_starthorizontalSlider.setEnabled(False)
        self.startTrimming.setEnabled(False)
        self.startTrimlabel.setEnabled(False)
        self.endTrimlabel.setEnabled(False)
        self.selectStartVideo.setEnabled(False)
        self.selectEndVideo.setEnabled(False)
        self.playTrim.setEnabled(False)

    def onSelectTrimVideo(self):

        self.trimFilename, _ = QFileDialog.getOpenFileName(self, "Open Video to Trim",directory=QtCore.QDir.currentPath())
        print(self.trimFilename)
        if self.trimFilename is not None and self.trimFilename != "":
            self.trimThread = TrimVideoThread(self.trimFilename)
            self.trimmer_starthorizontalSlider.setMaximum(self.trimThread.endFrame)
            self.trimmer_endhorizontalSlider.setMaximum(self.trimThread.endFrame)
            self.trimmer_endhorizontalSlider.setValue(self.trimThread.endFrame)
            self.trimmer_starthorizontalSlider.setEnabled(True)
            self.trimmer_endhorizontalSlider.setEnabled(True)
            self.startTrimming.setEnabled(True)
            self.startTrimlabel.setEnabled(True)
            self.endTrimlabel.setEnabled(True)
            self.selectStartVideo.setEnabled(True)
            self.selectEndVideo.setEnabled(True)
            self.playTrim.setEnabled(True)
            self.trimThread.change_pixmap_trim.connect(self.update_Trimvideoimage)
            self.trimThread.start()
        else:
            self.trimmer_starthorizontalSlider.setEnabled(False)
            self.trimmer_endhorizontalSlider.setEnabled(False)
            self.startTrimming.setEnabled(False)
            self.startTrimlabel.setEnabled(False)
            self.endTrimlabel.setEnabled(False)
            self.selectStartVideo.setEnabled(False)
            self.selectEndVideo.setEnabled(False)
            self.playTrim.setEnabled(False)
            self.onError("Some Error Occured")

    def startChanged(self):
        startValue = self.trimmer_starthorizontalSlider.value()
        endValue = self.trimmer_endhorizontalSlider.value()
        self.trimThread.startTrimFrame = startValue
        self.trimThread.frameId = startValue
        self.trimThread.framePosUpdated = True
        print("startValue",startValue)
        if(startValue >= endValue):
            self.trimmer_endhorizontalSlider.setValue(startValue)
            self.trimThread.endTrimFrame = endValue
    
    def endChanged(self):
        startValue = self.trimmer_starthorizontalSlider.value()
        endValue = self.trimmer_endhorizontalSlider.value()
        self.trimThread.endTrimFrame = endValue
        if(endValue <= startValue):
            self.trimmer_endhorizontalSlider.setValue(startValue)
            self.trimThread.startTrimFrame = startValue
        

    def update_Trimvideoimage(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.trimvideo_label.setScaledContents(True)
        self.trimvideo_label.setPixmap(qt_img)
        if self.trimThread.frameId>=self.trimThread.endTrimFrame-1:
            time.sleep(1)
            self.onTrimOpEnd()

    def onPlay(self):
        self.trimThread.isPlay = True if (self.trimThread.isPlay == False) else False
        if self.trimThread.isPlay == True:
            self.playTrim.setText("Pause")
        else:
            self.playTrim.setText("Play")

    def onTrimOpEnd(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Trimming Successful")
        msg.exec_()
        self.trimvideo_label.setPixmap(QtGui.QPixmap("Video Trimmer.png"))
    
    def onStartTrim(self):
        self.trimmer_starthorizontalSlider.setEnabled(False)
        self.trimmer_endhorizontalSlider.setEnabled(False)
        self.playTrim.setEnabled(False)
        self.trimThread.isPlay = False
        self.trimThread.isTrim = True
        date = datetime.datetime.now()
        self.trimThread.out = cv2.VideoWriter('Trimmed_Video_%s-%s-%sT%s-%s-%s.avi'%(date.year,date.month,date.day,date.hour,date.minute,date.second), self.trimThread.fourcc, self.trimThread.fps, (self.trimThread.cv_img.shape[1], self.trimThread.cv_img.shape[0]))
        

    
#end of trim functions



    def onError(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error Occured")
        msg.setInformativeText(error)
        msg.setWindowTitle("Error")
        msg.exec_()

    def show_file_info(self):
        fi = QFileInfo(self.thread.filename)
        size = ((int(fi.size())/1024)/1024)
        msg=QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Video File Information")
        a="FPS: {}\nFrame Count : {}\nVideo Format : {}\nVideo Duration : {}\nFile Size : {:.2f} MB".format(math.ceil(self.thread.fps), self.thread.frameCount, self.filename[-3:], self.thread.duration, size)
        msg.setText(a)
        x=msg.exec_()

    def onRename(self):
        try:
            fn, _ = QFileDialog.getOpenFileName(self, "Select file you want to rename",directory=QtCore.QDir.currentPath())
            directory = QFileDialog.getExistingDirectory(self, "Select File Directory", directory=QtCore.QDir.currentPath())
            fnOnly = os.path.basename(str(fn))
            print(fnOnly, fn, directory)
            text, ok = QInputDialog.getText(self, 'Rename', 'Enter new file name with extension', QLineEdit.Normal, fnOnly)
            print(text)
            if ok:
                print(fn, directory+"/"+text)
                os.rename(fn,directory+"/"+text)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Renaming Successful")
                msg.exec_()
        except Exception as e:
            self.onError(str(e))

    def onchange(self):
        self.isplaying =  self.thread.change_isplaying()
        if self.isplaying:
            self.statusbar.showMessage(self.filename+" is being played")
        else:
            self.statusbar.showMessage(self.filename+" is paused")
        self.pauseButton.setEnabled(self.isplaying)
        self.playButton.setEnabled(not self.isplaying)

    def onAlternate(self):
        self.thread.toggle_alternate()
        self.statusbar.showMessage("Skipping Frames By 1")

    def onScreenshot(self):
        self.thread.screenshotState()
        self.statusbar.showMessage("Screenshot saved to \"Screenshots\" Folder.")
       
    def onVideoEnd(self):
        print("VideoEnded")
        self.playButton.setEnabled(False)
        self.actionOpen.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.alternateFrames.setEnabled(False)
        self.alternateFrames.setChecked(False)
        self.screenshotButton.setEnabled(False)
        self.actionSave_Frames.setEnabled(False)
        self.horizontalSlider.setEnabled(False)
        self.actionVideo_Info.setEnabled(False)
        self.actionRename.setEnabled(True)
        self.actionLiveFeed.setEnabled(True)
        self.endLabel.setText("-- : -- : --")
        self.statusbar.showMessage("Video Ended")
        endtiming = time.time()
        time.sleep(1.5)
        self.video_label.setPixmap(QtGui.QPixmap("background.png"))
        print("Video End time", endtiming)
        print("Video Time Difference: {}".format (endtiming-self.thread.starttiming))

    def horizontalSliderPressed(self):
        # print("Pressed")
        self.sliderBusy = True 

    def horizontalSliderReleased(self):
        # print("Released")
        frame = self.horizontalSlider.value()
        self.thread.frameId = frame
        self.thread.framePosUpdated = True
        self.sliderBusy = False

    def sliderValueChanged(self):
        frame = self.horizontalSlider.value()
        self.thread.frameId = frame
        # print("ValueChanged",frame)

    def onLiveFeedMode(self):
        self.mergeFrame.hide()
        self.Trimframe.hide()
        self.video_label.show()
        self.actionOpen.setEnabled(False)
        self.actionVideoPlayer.setEnabled(True)
        self.actionLiveFeed.setEnabled(False)
        time.sleep(1.5)
        self.videoPlayerFrame.hide()
        self.liveFrame.show()
        self.livethread = LiveVideoThread()
        self.livethread.change_pixmap.connect(self.update_livevideoimage)
        self.livethread.start()

    def update_livevideoimage(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.video_label.setScaledContents(True)
        self.video_label.setPixmap(qt_img)
        if self.livethread.isLive ==  False:
            self.video_label.setPixmap(QtGui.QPixmap("background.png"))
 

    def onVideoPlayerMode(self):
        try:
            if isinstance(self.livethread, LiveVideoThread):
                self.livethread.isLive = False
            self.Trimframe.hide()
            self.video_label.show()
            self.mergeFrame.hide()
            self.actionMerge.setEnabled(True)
            self.actionLiveFeed.setEnabled(True)
            self.actionOpen.setEnabled(True)
            self.actionVideoPlayer.setEnabled(True)
            time.sleep(1.5)
            self.liveFrame.hide()
            self.videoPlayerFrame.show()
        except:
            self.onError("Some Error Occured")

    def onStartRecord(self):
        self.startRecordButton.setEnabled(False)
        self.stopRecordingButton.setEnabled(True)
        self.liveFeedFolder.setEnabled(False)
        date = datetime.datetime.now()
        if self.livethread.filepath == None:
            self.livethread.out = cv2.VideoWriter('Video_%s-%s-%sT%s-%s-%s.avi'%(date.year,date.month,date.day,date.hour,date.minute,date.second), self.livethread.fourcc, 15, (640, 480))
            print("1")
        else:
            self.pathname = "Video_%s-%s-%sT%s:%s:%s.avi"%(date.year,date.month,date.day,date.hour,date.minute,date.second)
            print(self.pathname)
            self.livethread.out = cv2.VideoWriter(self.pathname, self.livethread.fourcc, 15, (640, 480))
        self.livethread.isRecord = True
        self.statusbar.showMessage("Recording Started")
    
    def onStopRecord(self):
        self.startRecordButton.setEnabled(True)
        self.stopRecordingButton.setEnabled(False)
        self.liveFeedFolder.setEnabled(True)
        self.livethread.isRecord = False
        time.sleep(1)
        if self.livethread.filepath is not None:
            shutil.move(self.pathname, self.livethread.filepath)
        self.livethread.filepath = None
        self.statusbar.showMessage("Recording Stopped")

    def onLiveFeedFolder(self):
        try:
            directory = QFileDialog.getExistingDirectory(self, "Open Directory", directory=QtCore.QDir.currentPath()) 
            if self.livethread.filepath is None:
                self.livethread.filepath = directory
                self.statusbar.showMessage("FilePath: "+ directory)  
            else:
                self.onError("Try Again")  
        except Exception as e:
            self.onError(str(e))
    
    def on_exit(self):
        qApp.quit()

    
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.video_label.setScaledContents(True)
        self.video_label.setPixmap(qt_img)
        self.horizontalSlider.setValue(self.thread.frameId)
        if self.thread.frameId>=self.thread.endFrame:
            self.onVideoEnd()
        
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)


    def open_file(self):
        try:
            self.actionLiveFeed.setEnabled(False)
            self.videoPlayerFrame.setEnabled(True)
            self.alternateFrames.setChecked(False)
            self.screenshotButton.setEnabled(False)
            self.actionRename.setEnabled(False)
            self.actionSave_Frames.setEnabled(False)
            self.actionVideo_Info.setEnabled(False)
            self.endLabel.setText("-- : -- : --")
            self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video",directory=QtCore.QDir.currentPath())
            print(self.filename)
            if self.filename is not None and self.filename != "":
                self.statusbar.showMessage("Video Selected: "+self.filename)
                self.isplaying = True
                self.thread = VideoThread(self.filename, self.isplaying, self.isalternate, self.isScreenshot)
                self.horizontalSlider.setMinimum(self.thread.startFrame)
                self.horizontalSlider.setMaximum(self.thread.endFrame)
                self.pauseButton.setEnabled(True)
                self.alternateFrames.setEnabled(True)
                self.alternateFrames.setChecked(False)
                self.screenshotButton.setEnabled(True)
                self.actionVideo_Info.setEnabled(True)
                self.horizontalSlider.setEnabled(True)
                self.actionSave_Frames.setEnabled(True)
                self.actionOpen.setEnabled(False)
                self.actionVideoPlayer.setEnabled(False)
                self.endLabel.setText(self.thread.duration)
                self.thread.change_pixmap_signal.connect(self.update_image)
                self.thread.start()    
            else:
                self.onError("Select suitable video file.")
                self.playButton.setEnabled(False)
                self.actionOpen.setEnabled(True)
                self.pauseButton.setEnabled(False)
                self.alternateFrames.setEnabled(False)
                self.alternateFrames.setChecked(False)
                self.screenshotButton.setEnabled(False)
                self.actionSave_Frames.setEnabled(False)
                self.horizontalSlider.setEnabled(False)
                self.actionVideo_Info.setEnabled(False)
                self.actionRename.setEnabled(True)
                self.actionLiveFeed.setEnabled(True)
                self.actionVideoPlayer.setEnabled(False)
                self.endLabel.setText("-- : -- : --")
        except Exception as e:
            self.onError("Try Again")

    def onSaveFrames(self):
        try:
            directory = QFileDialog.getExistingDirectory(self, "Open Directory", directory=QtCore.QDir.currentPath()) 
            if directory is not None and directory != "":
                self.thread.saveFrames(directory, 0)
                self.statusbar.showMessage("Saved frames successfully in", directory)
                print("Saved frames successfully in", directory)
            else:
                self.onError("Invalid Directory")
        except Exception as e:
            self.onError("Try Again")

    def retranslateUi(self, QtPlayer):
        _translate = QtCore.QCoreApplication.translate
        QtPlayer.setWindowTitle(_translate("QtPlayer", "TIFR QtPlayer"))
        self.liveFeedFolder.setText(_translate("Qtplayer","Select folder"))
        self.startRecordButton.setText(_translate("Qtplayer","Start Recording"))
        self.stopRecordingButton.setText(_translate("Qtplayer","Stop Recording"))
        self.playButton.setText(_translate("QtPlayer", "Play"))
        self.pauseButton.setText(_translate("QtPlayer", "Pause"))
        self.screenshotButton.setText(_translate("QtPlayer", "Take Screenshot"))
        self.alternateFrames.setText(_translate("QtPlayer", "Alternate Frames"))
        self.startLabel.setText(_translate("QtPlayer", "00:00:00"))
        self.endLabel.setText(_translate("QtPlayer", "-- : -- : --"))
        self.menuMenu.setTitle(_translate("QtPlayer", "Menu"))
        self.menuEdit.setTitle(_translate("QtPlayer", "Edit"))
        self.actionOpen.setText(_translate("QtPlayer", "Open"))
        self.actionOpen.setStatusTip(_translate("QtPlayer", "Open A Video"))
        self.actionOpen.setShortcut(_translate("QtPlayer", "Ctrl+N"))
        self.actionRename.setText(_translate("QtPlayer", "Save as"))
        self.actionRename.setShortcut(_translate("QtPlayer", "Ctrl+S"))
        self.actionVideo_Info.setText(_translate("QtPlayer", "Video Info."))
        self.actionVideoPlayer.setText(_translate("QtPlayer", "VideoPlayer"))
        self.actionVideoPlayer.setStatusTip(_translate("QtPlayer", "VideoPlayer Mode"))
        self.actionLiveFeed.setText(_translate("QtPlayer", "Live Camera"))
        self.actionLiveFeed.setStatusTip(_translate("QtPlayer", "Camera Mode"))
        self.actionExit_Player.setText(_translate("QtPlayer", "Exit Player"))
        self.actionExit_Player.setShortcut(_translate("QtPlayer", "Ctrl+X"))
        self.actionTrim.setText(_translate("QtPlayer", "Trim"))
        self.actionMerge.setText(_translate("QtPlayer", "Merge"))
        self.actionSave_Frames.setText(_translate("QtPlayer", "Save Frames"))
        self.heading.setText(_translate("QtPlayer", "QT Video Merger"))
        self.file_open1.setText(_translate("QtPlayer", "Open File"))
        self.file_open2.setText(_translate("QtPlayer", "Open File"))
        self.video1select.setText(_translate("QtPlayer", "Select Video 1"))
        self.start_merge.setText(_translate("QtPlayer", "Start Merging!"))
        self.video2select.setText(_translate("QtPlayer", "Select Video 2"))

        #trim ui
        self.trimVideoSelect.setText(_translate("MainWindow", "Select Video"))
        self.startTrimming.setText(_translate("MainWindow", "Start Trimming"))
        self.selectStartVideo.setText(_translate("MainWindow", "Select Start"))
        self.selectEndVideo.setText(_translate("MainWindow", "Select End"))
        self.startTrimlabel.setText(_translate("MainWindow", "Start"))
        self.endTrimlabel.setText(_translate("MainWindow", "End"))
        self.playTrim.setText(_translate("MainWindow", "Play"))


class VideoThread(QThread, Ui_QtPlayer):
    change_pixmap_signal = pyqtSignal(np.ndarray)
        
    def __init__(self, filename, isplaying, isalternate, isScreenshot):
        super().__init__()
        self.filename = filename
        self._run_flag = True
        self.duration = 0
        self.isplaying = isplaying
        self.frameId = 0
        self.startFrame = 0
        self.starttiming = 0

        self.cap = cv2.VideoCapture(self.filename)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frameCount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.endFrame = self.frameCount-1
        self.secsDuration = self.frameCount/self.fps
        self.framePosUpdated = False
        print('fps = ' + str(self.fps))
        print('Number of frames = ' + str(self.frameCount))
        secs = self.secsDuration
        self.duration = time.strftime('%H:%M:%S', time.gmtime(secs))
        print("Duration (H:M:S) = ", self.duration)
        print("Wait Key Value",int(1000/self.fps))

        self.isalternate = isalternate
        self.isScreenshot = isScreenshot

    def toggle_alternate(self):
        self.isalternate =  False if (self.isalternate==True) else True

    def change_isplaying(self):
        self.isplaying =  False if (self.isplaying==True) else True
        return self.isplaying

    def screenshotState(self):
        self.isScreenshot = True

    def run(self):
        try:
            altIncrement = 2
            font = cv2.FONT_HERSHEY_SIMPLEX 
            org = (00, 30)  
            fontScale = 1
            color = (0, 0, 255) 
            thickness = 2
            self.starttiming = time.time()
            print("Video start time", self.starttiming)
            while self._run_flag and self.cap.isOpened():
                if self.isplaying or self.framePosUpdated:
                    if self.framePosUpdated:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameId)
                        self.framePosUpdated=False
                    if self.isalternate:
                        for _ in range(altIncrement):
                            ret, cv_img = self.cap.read()
                        if ret:
                            image = cv2.putText(cv_img, str(self.frameId), org, font, fontScale,  
                                            color, thickness, cv2.LINE_AA, False)
                            self.change_pixmap_signal.emit(cv_img)
                            if self.isScreenshot:
                                cv2.imwrite(screenshots_dir + "\\frame%d.jpg" % self.frameId, image)
                                self.isScreenshot = False
                            self.frameId+=altIncrement
                    else:
                        ret, cv_img = self.cap.read()
                        if ret:
                            image = cv2.putText(cv_img, str(self.frameId), org, font, fontScale,  
                                            color, thickness, cv2.LINE_AA, False)
                            self.change_pixmap_signal.emit(cv_img)
                            if self.isScreenshot:
                                cv2.imwrite(screenshots_dir + "\\frame%d.jpg" % self.frameId, image)
                                self.isScreenshot = False
                            cv2.waitKey(int(1000/self.fps))
                            self.frameId+=1
                if self.frameCount<=self.frameId:
                    self._run_flag = False
            self.cap.release()
        except Exception as e:
            self.onError(self,str(e))

    def saveFrames(self, directory, frameId=0):
        cap = self.cap
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameId)
        while True:
            ret, frame = cap.read()
            if ret is False:
                break
            cv2.imwrite(os.path.join(directory,"frame{:d}.jpg".format(frameId)), frame)
            frameId += 1
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class LiveVideoThread(QThread, Ui_QtPlayer):
    change_pixmap = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.isLive = True
        self.isRecord = False
        self.filepath = None
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    def run(self):
        try:
            while self._run_flag and self.isLive:
                ret, cv_img = self.cap.read()
                if ret:
                    self.change_pixmap.emit(cv_img)
                if self.isRecord:
                    self.out.write(cv_img)
            self.cap.release()
            self.out.release()
        except Exception as e:
            print(str(e))
 
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class TrimVideoThread(QThread, Ui_QtPlayer):
    change_pixmap_trim = pyqtSignal(np.ndarray)

    def __init__(self, trimFileName):
        super().__init__()
        self._run_flag = True
        self.isPlay = False
        self.trimFileName = trimFileName
        self.frameId = 0
        self.cap = cv2.VideoCapture(self.trimFileName)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frameCount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.endFrame = self.frameCount-1
        self.startTrimFrame = 0
        self.startFrame = 0
        self.endTrimFrame = self.endFrame
        self.secsDuration = self.frameCount/self.fps
        self.framePosUpdated = False
        self.isTrim = False
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.cv_img = None

        print('fps = ' + str(self.fps))
        print('Number of frames = ' + str(self.frameCount))
        secs = self.secsDuration
        self.duration = time.strftime('%H:%M:%S', time.gmtime(secs))
        print("Duration (H:M:S) = ", self.duration)
        print("Wait Key Value",int(1000/self.fps))

    def run(self):
        trimStarted = True
        self.frameId = self.startTrimFrame
        ret, self.cv_img = self.cap.read()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameId)
        self.change_pixmap_trim.emit(self.cv_img)
        print(self.cv_img.shape)
        while self._run_flag:
            if self.isTrim and trimStarted:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.startTrimFrame)
                print("STarted")
                self.frameId = self.startTrimFrame
                trimStarted = False
                print(self.endTrimFrame)
            if self.isTrim and self.frameId<=self.endTrimFrame:
                ret, self.cv_img = self.cap.read()
                if ret:
                    self.change_pixmap_trim.emit(self.cv_img)
                    self.out.write(self.cv_img)
                    print(self.frameId)
                    self.frameId+=1
            if self.frameId>=self.endTrimFrame:
                break

            if self.isPlay or self.framePosUpdated and not self.isTrim:
                if self.framePosUpdated:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameId)
                    self.framePosUpdated=False    
                ret, self.cv_img = self.cap.read()
                if ret  and not self.isTrim:
                    self.change_pixmap_trim.emit(self.cv_img)
                    self.frameId+=1
                    cv2.waitKey(int(1000/self.fps))
        print("Done")
        self.out.release()
        self.cap.release()
        
 
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.exit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtPlayer = QtWidgets.QMainWindow()
    ui = Ui_QtPlayer()
    ui.setupUi(QtPlayer)
    QtPlayer.show()
    sys.exit(app.exec_())