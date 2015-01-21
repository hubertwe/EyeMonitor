import wx

typeEVT_FRAME = wx.NewEventType()
EVT_FRAME = wx.PyEventBinder(typeEVT_FRAME, 1)

typeEVT_EYES = wx.NewEventType()
EVT_EYES = wx.PyEventBinder(typeEVT_EYES, 1)

class FrameEvent(wx.PyCommandEvent):

    def __init__(self, frame):
        wx.PyCommandEvent.__init__(self, typeEVT_FRAME, -1)
        self.frame = frame

    def GetFrame(self):
        return self.frame

class EyesEvent(wx.PyCommandEvent):

    def __init__(self, message, counter):
        wx.PyCommandEvent.__init__(self, typeEVT_EYES, -1)
        self.message = message
        self.counter = counter

    def GetMessage(self):
        return self.message

    def GetCounter(self):
        return self.counter