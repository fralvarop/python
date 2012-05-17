#Boa:Frame:FrameSecond

import wx

def create(parent):
    return FrameSecond(parent)

[wxID_FRAMESECOND, wxID_FRAMESECONDBTNFSSALIR, wxID_FRAMESECONDPANEL1, 
 wxID_FRAMESECONDSTHOLA, 
] = [wx.NewId() for _init_ctrls in range(4)]

class FrameSecond(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMESECOND, name=u'FrameSecond',
              parent=prnt, pos=wx.Point(430, 252), size=wx.Size(461, 258),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Segunda ventana')
        self.SetClientSize(wx.Size(461, 258))
        self.Center(wx.BOTH)

        self.panel1 = wx.Panel(id=wxID_FRAMESECONDPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(461, 258),
              style=wx.TAB_TRAVERSAL)

        self.btnFSSalir = wx.Button(id=wxID_FRAMESECONDBTNFSSALIR,
              label=u'Salir', name=u'btnFSSalir', parent=self.panel1,
              pos=wx.Point(182, 171), size=wx.Size(85, 29), style=0)
        self.btnFSSalir.Bind(wx.EVT_BUTTON, self.OnBtnFSSalirClick,
              id=wxID_FRAMESECONDBTNFSSALIR)

        self.stHola = wx.StaticText(id=wxID_FRAMESECONDSTHOLA,
              label=u'Hola, soy la segunda ventana', name=u'stHola',
              parent=self.panel1, pos=wx.Point(76, 71), size=wx.Size(321, 23),
              style=0)
        self.stHola.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'Sans'))

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.parent = parent

    def OnBtnFSSalirClick(self, event):
        self.parent.Show()
        self.Hide()
