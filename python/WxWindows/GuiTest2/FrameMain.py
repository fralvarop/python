#Boa:Frame:FrameMain

import wx
import FrameSecond

def create(parent):
    return FrameMain(parent)

[wxID_FRAMEMAIN, wxID_FRAMEMAINBTNMUESTRANUEVA, wxID_FRAMEMAINBTNSALIR, 
 wxID_FRAMEMAINPANEL1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class FrameMain(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMEMAIN, name=u'FrameMain',
              parent=prnt, pos=wx.Point(695, 336), size=wx.Size(400, 340),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Ventana principal')
        self.SetClientSize(wx.Size(400, 340))
        self.Center(wx.BOTH)

        self.panel1 = wx.Panel(id=wxID_FRAMEMAINPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(400, 340),
              style=wx.TAB_TRAVERSAL)

        self.btnMuestraNueva = wx.Button(id=wxID_FRAMEMAINBTNMUESTRANUEVA,
              label=u'Mostrar la otra ventana', name=u'btnMuestraNueva',
              parent=self.panel1, pos=wx.Point(104, 123), size=wx.Size(192, 29),
              style=0)
        self.btnMuestraNueva.Bind(wx.EVT_BUTTON, self.OnBtnMuestraNuevaClick,
              id=wxID_FRAMEMAINBTNMUESTRANUEVA)

        self.btnSalir = wx.Button(id=wxID_FRAMEMAINBTNSALIR, label=u'Salir',
              name=u'btnSalir', parent=self.panel1, pos=wx.Point(155, 192),
              size=wx.Size(85, 29), style=0)
        self.btnSalir.Bind(wx.EVT_BUTTON, self.OnBtnSalirClick,
              id=wxID_FRAMEMAINBTNSALIR)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.Fs=FrameSecond.FrameSecond(self)

    def OnBtnMuestraNuevaClick(self, event):
        self.Fs.Show()
        self.Hide()

    def OnBtnSalirClick(self, event):
        self.Close()
