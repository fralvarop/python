#Boa:Frame:Frame1
# -*- coding: utf-8 -*-

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BTNMUESTRADIALOGO, wxID_FRAME1PANEL1, 
] = [wx.NewId() for _init_ctrls in range(3)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(481, 338), size=wx.Size(349, 172),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Mi primer GUI')
        self.SetClientSize(wx.Size(349, 172))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(349, 172),
              style=wx.TAB_TRAVERSAL)

        self.btnMuestraDialogo = wx.Button(id=wxID_FRAME1BTNMUESTRADIALOGO,
              label=u'Haz clic aqu\xed', name=u'btnMuestraDialogo',
              parent=self.panel1, pos=wx.Point(112, 63), size=wx.Size(118, 29),
              style=0)
        self.btnMuestraDialogo.Bind(wx.EVT_BUTTON,
              self.OnBtnMuestraDialogoBoton, id=wxID_FRAME1BTNMUESTRADIALOGO)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnBtnMuestraDialogoBoton(self, event):
        #event.Skip()
        #wx.MessageBox('Has hecho clic en el botón', 'Aviso', wx.ICON_QUESTION)
        #wx.MessageBox('Has hecho clic en el botón', 'Aviso', wx.ICON_EXCLAMATION)
        #wx.MessageBox('Has hecho clic en el botón', 'Aviso', wx.ICON_ERROR)
        wx.MessageBox('Has hecho clic en el botón', 'Aviso', wx.ICON_INFORMATION)
