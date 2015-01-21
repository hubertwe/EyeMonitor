from VideoProcessor import *

class EyeMonitor(wx.Frame):
    def __init__(self, parent=None, title="Eyes Monitor", size=(640,480), fps=24):
        wx.Frame.__init__(self, parent, title=title, size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self._bitmap = None
        self._size = size
        self._fps = fps
        self._videoProcessor = VideoProcessor(self, size, fps)
        self.Bind(wx.EVT_PAINT, self._repaint)
        self.Bind(wx.EVT_CLOSE, self._close)
        self.Bind(EVT_FRAME, self._display)
        self.Bind(EVT_EYES, self._alert)
        self._createMenuBar()
        self.Show(True)

    def _createMenuBar(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        settings = wx.MenuItem(file, 101, '&Setting', 'Open a new document')
        file.AppendItem(settings)
        file.AppendSeparator()
        quit = wx.MenuItem(file, wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit the Application')
        file.AppendItem(quit)
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        self._statusBar = self.CreateStatusBar()
        self._statusBar.SetStatusText('Sleeps counter: 0')

        self.Bind(wx.EVT_MENU, self._quit, quit)
        self.Bind(wx.EVT_MENU, self._settings, settings)

    def _repaint(self, evt):
        if self._bitmap is None:
            return
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self._bitmap, 0, 0)

    def _display(self, event):
        self._bitmap = event.GetFrame()
        self.Refresh()

    def _alert(self, event):
        self._statusBar.SetStatusText('Sleeps counter: ' + str(event.GetCounter()) + '     ' + str(event.GetMessage()))
        '''
        dlg = wx.MessageDialog(self, event.GetValue(), 'Wake Up',
            wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        '''

    def _close(self, event):
        self._videoProcessor.stop()
        self.Destroy()

    def _quit(self, event):
        self.Close()

    def _settings(self, event):
        print 'dupa'

if __name__ == "__main__":
    app = wx.App()
    eyeMonitor = EyeMonitor()
    app.MainLoop()