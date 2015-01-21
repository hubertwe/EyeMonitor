import cv
import cv2 as opencv
import threading
from Events import *
import time

class VideoProcessor(threading.Thread):

    def __init__(self, parent, size, fps):
        threading.Thread.__init__(self)
        self._parent = parent
        self._faceCascade = opencv.CascadeClassifier('haarcascade_frontalface_default.xml')
        self._eyeCascade = opencv.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
        self._video = None
        self._width = size[0]
        self._height = size[1]
        self._fps = fps
        self._eyesTimer = None
        self._isStopped = False
        self._sleepsCount = 0
        self._isSleeping = False
        self.start()

    def run(self):
        self._video = opencv.VideoCapture(0)
        self._video.set(cv.CV_CAP_PROP_FRAME_WIDTH, self._width)
        self._video.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self._height)
        while(not self._isStopped):
            time.sleep(1/self._fps)
            self._nextFrame()

    def stop(self):
        self._isStopped = True
        self.join()

    def _nextFrame(self):
        ret, frame = self._video.read()
        if ret:
            frame = self._detectFace(frame)
            bitmap = wx.BitmapFromBuffer(self._width, self._height, frame)
            event = FrameEvent(bitmap)
            wx.PostEvent(self._parent, event)

    def _detectFace(self, frame):
        gray = opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)
        faces = self._faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            opencv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self._eyeCascade.detectMultiScale(roi_gray, 1.4, 4)
            if len(eyes) != 0 and self._eyesTimer:
                self._eyesClosed(False)
            elif len(eyes) == 0 and not self._eyesTimer:
                self._eyesTimer = self._startTimer(2, self._eyesClosed)
            for (ex,ey,ew,eh) in eyes:
                opencv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        if self._isSleeping:
            #opencv.rectangle(frame,(0,0),(self._width-8,self._height),(0,0,255),30)
            opencv.putText(frame,"Wake Up!!!", (self._width/2-150,self._height/2-50), opencv.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), thickness=6)
        return opencv.cvtColor(frame, opencv.COLOR_BGR2RGB)

    def _eyesClosed(self, closed=True):
        if closed:
            self._sleepsCount += 1;
            self._isSleeping = True
            event = EyesEvent('Wake Up!', self._sleepsCount)
        else:
            self._isSleeping = False
            event = EyesEvent('', self._sleepsCount)
            self._eyesTimer.cancel()
            self._eyesTimer = None
        wx.PostEvent(self._parent, event)

    def _startTimer(self, seconds, callback):
        timer = threading.Timer(seconds, callback)
        timer.start()
        return timer