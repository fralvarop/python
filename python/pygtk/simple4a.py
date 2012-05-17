#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class Simple:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event", self.delete_event)

        self.box1 = gtk.HBox(False, 0)
        self.window.add(self.box1)
        self.button = gtk.Button("Botón 1")
        self.button.connect("clicked", self.btn1Clicked, None)
        self.box1.pack_start(self.button, True, True, 0)
        self.button.show()

        self.button2 = gtk.Button("Botón 2")
        self.button2.connect("clicked", self.btn2Clicked, None)
        self.box1.pack_start(self.button2, True, True, 0)
        self.button2.show()

        self.box1.show()

        self.window.show()

    def main(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def btn1Clicked(self, widget, data=None):
        print 'Pulsado el botón 1'
        #gtk.main_quit()

    def btn2Clicked(self, widget, data=None):
        print 'Pulsado el botón 2'

if __name__ == "__main__":
    simple = Simple()
    simple.main()

