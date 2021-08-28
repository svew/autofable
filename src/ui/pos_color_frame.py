import wx
import threading
import time


class PosColorToolFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None, 
            title='Position and Color Tool', 
            size=(360, 320), 
            style=(wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        )
        self.SetWindowStyle
        
        panel = wx.Panel(self)
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.__color_text = wx.StaticText(panel, 
            label="Color: ", 
            pos=(30,30)
        )
        self.__empty_img = wx.EmptyImage(333,200)
        self.__image_ctrl = wx.StaticBitmap(panel, 
            bitmap=wx.BitmapFromImage(self.__empty_img),
            style=wx.ALIGN_CENTER
        )

        # GUI wrapup
        panel.SetSizer(self.__main_sizer)
        panel.Layout() 

        thread = threading.Thread(target=self.__run)
        thread.start()

    def __run(self):
        while True:
            time.sleep(1)
            self.__color_text.LabelText += "A"

if __name__ == '__main__':
    app = wx.App(False)
    frame = PosColorToolFrame()
    frame.Show()
    app.MainLoop()