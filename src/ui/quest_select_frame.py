
import wx
from autofable import AutoFable
from pos_color_tool_frame import PosColorToolFrame

'''
AutoFable  _ [] X

Textbox
Listbox
Searchbox
Multiple text boxes
Image


'''

POS_COLOR_TOOL_ID = 0
NO_BOTTOM = wx.TOP | wx.LEFT | wx.RIGHT

class QuestSelectFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='AutoFable', size=(300, 600))
        
        panel = wx.Panel(self)
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Menu bar
        menubar = wx.MenuBar()
        tool_menu = wx.Menu()
        pos_color_tool = wx.MenuItem(tool_menu, id=POS_COLOR_TOOL_ID, text="Position and Color Tool", 
            kind=wx.ITEM_NORMAL)
        tool_menu.Append(pos_color_tool)
        menubar.Append(tool_menu, '&Tools')
        self.Bind(wx.EVT_MENU, self.__menu_handler)
        self.SetMenuBar(menubar)

        # Intro text
        intro_textbox = wx.StaticText(panel, label='Select a mission', style=wx.ALIGN_CENTER)
        self.__main_sizer.Add(intro_textbox, 0, NO_BOTTOM | wx.EXPAND, 10)

        # Quests list
        self.__quests_listbox = wx.ListBox(panel, size=(-1, 160))
        self.__quests_listbox.Bind(wx.EVT_LISTBOX, self.__select_quest)
        self.__main_sizer.Add(self.__quests_listbox, 0, NO_BOTTOM | wx.EXPAND, 10)

        # Search box
        self.__search_ctrl = wx.SearchCtrl(panel, size=(-1, -1), style=wx.BORDER_SUNKEN)
        self.__search_ctrl.Bind(wx.EVT_TEXT, self.__search_event)
        self.__main_sizer.Add(self.__search_ctrl, 0, NO_BOTTOM | wx.EXPAND, 10)

        # Quest title
        self.__title_textbox = wx.StaticText(panel, label=('█' * 10), style=wx.ALIGN_CENTER)
        self.__title_textbox.SetForegroundColour((210, 210, 210))
        title_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.__title_textbox.SetFont(title_font)
        self.__main_sizer.Add(self.__title_textbox, 0, wx.ALL | wx.EXPAND, 10)

        # Quest image
        self.__quest_image = wx.StaticBitmap(panel, size=(-1, 120), style=wx.BORDER_SUNKEN)
        self.__main_sizer.Add(self.__quest_image, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 30)

        # GUI wrapup
        panel.SetSizer(self.__main_sizer)
        panel.Layout()

        # Controller
        self.__autofable = AutoFable()
        self.__autofable.load()
        self.__quests_list = []
        self.__display_quests("")

    def __display_quests(self, query):
        self.__quests_list = [(quest.search_match(query), quest) for quest in self.__autofable.quests]
        list.sort(self.__quests_list, key=lambda quest: quest[0])
        self.__quests_listbox.Clear()
        print(self.__quests_list)
        for i, quest in enumerate(self.__quests_list):
            if quest[0] == float('inf'):
                break
            self.__quests_listbox.Insert(quest[1].name, i)

    def __search_event(self, event): 
        query = self.__search_ctrl.GetValue()
        self.__display_quests(query)

    def __select_quest(self, event):
        index = self.__quests_listbox.GetSelection()
        print(index)
        if index <= len(self.__quests_list):
            title = self.__quests_list[index][1].name
            self.__title_textbox.SetLabel(title)

    def __menu_handler(self, event):
        id = event.GetId()
        if id == POS_COLOR_TOOL_ID:
            print('opening')
            tool_frame = PosColorToolFrame()
            tool_frame.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = QuestSelectFrame()
    frame.Show()
    app.MainLoop()