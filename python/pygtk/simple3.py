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
        self.window.show()

    def main(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

if __name__ == "__main__":
    simple = Simple()
    simple.main()

