
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QFileDialog, QStyle, qApp, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QFileInfo
from threading import Timer,Thread,Event
import numpy as np
import time, os, sys, cv2, math, datetime

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

        self.frame1 = QtWidgets.QFrame(self.centralwidget)
        self.frame1.setGeometry(QtCore.QRect(10, 600, 1251, 121))
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame1")


        self.horizontalSlider = QtWidgets.QSlider(self.frame1)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setGeometry(QtCore.QRect(320, 30, 930, 41))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setEnabled(False)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(1)
        self.horizontalSlider.sliderPressed.connect(self.horizontalSliderPressed)
        self.horizontalSlider.sliderReleased.connect(self.horizontalSliderReleased)
        self.horizontalSlider.valueChanged.connect(self.sliderValueChanged)
        self.sliderBusy = False

        self.playButton = QtWidgets.QPushButton(self.frame1)
        self.playButton.setGeometry(QtCore.QRect(0, 30, 75, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.playButton.setFont(font)
        self.playButton.setEnabled(False)
        self.playButton.setObjectName("playButton")

        self.pauseButton = QtWidgets.QPushButton(self.frame1)
        self.pauseButton.setGeometry(QtCore.QRect(90, 30, 75, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pauseButton.setFont(font)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setObjectName("pauseButton")

        self.screenshotButton = QtWidgets.QPushButton(self.frame1)
        self.screenshotButton.setGeometry(QtCore.QRect(0, 80, 165, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.screenshotButton.setFont(font)
        self.screenshotButton.setEnabled(False)
        self.screenshotButton.setObjectName("screenshotButton")

        self.alternateFrames = QtWidgets.QCheckBox(self.frame1)
        self.alternateFrames.setGeometry(QtCore.QRect(170, 30, 161, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.alternateFrames.setEnabled(False)
        self.alternateFrames.setFont(font)
        self.alternateFrames.setObjectName("alternateFrames")

        self.startLabel = QtWidgets.QLabel(self.frame1)
        self.startLabel.setGeometry(QtCore.QRect(315, 80, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(60)
        self.startLabel.setFont(font)
        self.startLabel.setObjectName("startLabel")

        self.endLabel = QtWidgets.QLabel(self.frame1)
        self.endLabel.setGeometry(QtCore.QRect(1190, 70, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(60)
        self.endLabel.setFont(font)
        self.endLabel.setObjectName("endLabel")


        self.frame2 = QtWidgets.QFrame(self.centralwidget)
        self.frame2.setGeometry(QtCore.QRect(10, 600, 1251, 140))
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.hide()
        self.frame2.setObjectName("frame2")

        self.startRecordButton = QtWidgets.QPushButton(self.frame2)
        self.startRecordButton.setGeometry(QtCore.QRect(220, 20, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startRecordButton.setFont(font)
        self.startRecordButton.setEnabled(True)
        self.startRecordButton.setObjectName("startRecord")

        self.stopRecordingButton = QtWidgets.QPushButton(self.frame2)
        self.stopRecordingButton.setGeometry(QtCore.QRect(500, 20, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.stopRecordingButton.setFont(font)
        self.stopRecordingButton.setEnabled(False)
        self.stopRecordingButton.setObjectName("stopRecordingButton")

        self.liveFeedFolder = QtWidgets.QPushButton(self.frame2)
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
        self.actionVideoPlayer.setEnabled(False)
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

        self.retranslateUi(QtPlayer)
        QtCore.QMetaObject.connectSlotsByName(QtPlayer)


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
        self.actionOpen.setEnabled(False)
        self.actionVideoPlayer.setEnabled(True)
        self.actionLiveFeed.setEnabled(False)
        time.sleep(1.5)
        self.frame1.hide()
        self.frame2.show()
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
        self.livethread.isLive = False
        self.actionLiveFeed.setEnabled(True)
        self.actionOpen.setEnabled(True)
        self.actionLiveFeed.setEnabled(True)
        time.sleep(1.5)
        self.frame2.hide()
        self.frame1.show()


    def onStartRecord(self):
        self.startRecordButton.setEnabled(False)
        self.stopRecordingButton.setEnabled(True)
        self.liveFeedFolder.setEnabled(False)
        date = datetime.datetime.now()
        if self.livethread.filepath == None:
            self.livethread.out = cv2.VideoWriter('Video_%s-%s-%sT%s-%s-%s.avi'%(date.year,date.month,date.day,date.hour,date.minute,date.second), self.livethread.fourcc, 15, (640, 480))
            print("1")
        else:
            pathname = self.livethread.filepath+"/Video_%s-%s-%sT%s:%s:%s.avi"%(date.year,date.month,date.day,date.hour,date.minute,date.second)
            self.livethread.out = cv2.VideoWriter(pathname, self.livethread.fourcc, 15, (640, 480))
        self.livethread.isRecord = True
        self.statusbar.showMessage("Recording Started")
    
    def onStopRecord(self):
        self.startRecordButton.setEnabled(True)
        self.stopRecordingButton.setEnabled(False)
        self.liveFeedFolder.setEnabled(True)
        self.livethread.isRecord = False
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
            self.frame1.setEnabled(True)
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
        i = 0
        try:
            while self._run_flag and self.isLive:
                ret, cv_img = self.cap.read()
                if ret:
                    self.change_pixmap.emit(cv_img)
                    i+=1
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtPlayer = QtWidgets.QMainWindow()
    ui = Ui_QtPlayer()
    ui.setupUi(QtPlayer)
    QtPlayer.show()
    sys.exit(app.exec_())
