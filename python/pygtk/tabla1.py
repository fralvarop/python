#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class Table:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Prueba con tablas 1")
        self.window.set_border_width(20)
        self.window.set_size_request(250, 100)
        self.window.connect("delete_event", self.delete_event)
        table = gtk.Table(2, 2, True) # Tabla de 2x2
        self.window.add(table)

        button1 = gtk.Button("Botón 1")
        button1.connect("clicked", self.callback, "botón 1")
        table.attach(button1, 0, 1, 0, 1)
        button1.show()

        button2 = gtk.Button("Botón 2")
        button2.connect("clicked", self.callback, "botón 2")
        table.attach(button2, 1, 2, 0, 1)
        button2.show()

        button3 = gtk.Button("Salir")
        button3.connect("clicked", self.ExitApp, "botón 3")
        table.attach(button3, 0, 2, 1, 2)
        button3.show()

        table.show()
        self.window.show()

    def main(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def callback(self, widget, data=None):
        print 'Pulsado el %s' % data

    def ExitApp(self, widget, event, data=None):
        print 'Se ha pulsado el botón de salir'
        gtk.main_quit()

if __name__ == "__main__":
    table = Table()
    table.main()

