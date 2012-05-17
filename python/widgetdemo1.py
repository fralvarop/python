#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demostración de los widgets básicos de la biblioteca Tkinter

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

from Tkinter import *
import tkMessageBox

class Demo:
    """Clase que implementa los widgets básicos de la biblioteca Tkinter."""

    def __init__(self,master):
        """Inicializador de la clase Demo
        @param master: Ventana que contendrá el único frame
        @type master: Tkinter.Tk"""
        # Definimos las variables que utilizaremos
        self.ValorCheckbutton1 = IntVar()
        self.ValorCheckbutton2 = IntVar()
        self.ValorRadiobuttons1 = IntVar()
        self.ValorRadiobuttons2 = StringVar()
        self.Desactivado = False
        # Elementos para la lista
        self.ejemplos = ['Elemento uno', 'Elemento dos', 'Elemento tres', 'Elemento cuatro']

        frame = self.ConstruirWidgets(master)
        self.ColocarWidgets(frame)

    def ConstruirWidgets(self,master):
        """Construye los widgets a mostrar
        @param master: Frame maestro que contendrá al resto
        @type master: Tkinter.Frame
        @return: Frame maestro modificado"""
        frame = Frame(master)
        # Etiquetas
        self.lblframe = Frame(frame, relief = SUNKEN, padx = 3, pady = 3, borderwidth = 2, width = 500)
        self.lbl1 = Label(self.lblframe, text="Flat Label", relief = FLAT, width = 13, borderwidth = 2)
        self.lbl2 = Label(self.lblframe, text="Sunken Label", relief = SUNKEN, width = 13, borderwidth = 2)
        self.lbl3 = Label(self.lblframe, text="Ridge Label", relief = RIDGE, width = 13, borderwidth = 2)
        self.lbl4 = Label(self.lblframe, text="Raised Label", relief = RAISED, width = 13, borderwidth = 2)
        self.lbl5 = Label(self.lblframe, text="Groove Label", relief = GROOVE, width = 13, borderwidth = 2)

        # Botones
        self.btnframe = Frame(frame, relief = SUNKEN,padx = 3, pady = 3, borderwidth = 2, width = 500)
        self.btn1 = Button(self.btnframe, text="Flat Button", relief = FLAT, borderwidth = 2)
        self.btn2 = Button(self.btnframe, text="Sunken Button", relief = SUNKEN, borderwidth = 2)
        self.btn3 = Button(self.btnframe, text="Ridge Button", relief = RIDGE, borderwidth = 2)
        self.btn4 = Button(self.btnframe, text="Raised Button", relief = RAISED, borderwidth = 2)
        self.btn5 = Button(self.btnframe, text="Groove Button", relief = GROOVE, borderwidth = 2)
        self.btn1.bind('<ButtonRelease-1>', lambda e: self.BtnCallback('flat'))
        self.btn2.bind('<ButtonRelease-1>', lambda e: self.BtnCallback('sunken'))
        self.btn3.bind('<ButtonRelease-1>', lambda e: self.BtnCallback('ridge'))
        self.btn4.bind('<ButtonRelease-1>', lambda e: self.BtnCallback('raised'))
        self.btn5.bind('<ButtonRelease-1>', lambda e: self.BtnCallback('groove'))

        # Checkboxes
        self.cbframe = Frame(frame, relief = SUNKEN, padx = 3, pady = 3, borderwidth = 2, width = 500)
        self.chk1 = Checkbutton(self.cbframe, text = "Checkbox normal",variable=self.ValorCheckbutton1)
        self.chk2 = Checkbutton(self.cbframe, text = "Checkbox sin casilla",variable=self.ValorCheckbutton2,indicatoron = False)
        self.chk1.bind('<ButtonRelease-1>', lambda e: self.ChkBoxClick(1))
        self.chk2.bind('<ButtonRelease-1>', lambda e: self.ChkBoxClick(2))
        self.btnToggleCB = Button(self.cbframe,text="Conmutar checkboxes")
        self.btnToggleCB.bind('<ButtonRelease-1>', self.btnConmutar)

        # Radiobuttons
        self.rbframe = Frame(frame, relief = SUNKEN, padx = 3, pady = 3, borderwidth = 2, width = 500)
        self.rb1 = Radiobutton(self.rbframe, text = "Radio 1", variable = self.ValorRadiobuttons1, value = 1)
        self.rb2 = Radiobutton(self.rbframe, text = "Radio 2", variable = self.ValorRadiobuttons1, value = 2)
        self.rb3 = Radiobutton(self.rbframe, text = "Radio 3", variable = self.ValorRadiobuttons1, value = 3)
        self.rb1.bind('<ButtonRelease-1>', lambda e: self.RBClick1())
        self.rb2.bind('<ButtonRelease-1>', lambda e: self.RBClick1())
        self.rb3.bind('<ButtonRelease-1>', lambda e: self.RBClick1())
        self.rb4 = Radiobutton(self.rbframe, text = "Radio 1-1", variable = self.ValorRadiobuttons2, value = "1-1")
        self.rb5 = Radiobutton(self.rbframe, text = "Radio 1-2", variable = self.ValorRadiobuttons2, value = "1-2")
        self.rb6 = Radiobutton(self.rbframe, text = "Radio 1-3", variable = self.ValorRadiobuttons2, value = "1-3")
        self.rb4.bind('<ButtonRelease-1>', lambda e: self.RBClick2())
        self.rb5.bind('<ButtonRelease-1>', lambda e: self.RBClick2())
        self.rb6.bind('<ButtonRelease-1>', lambda e: self.RBClick2())

        # Cajas de texto
        self.tbframe = Frame(frame, relief = SUNKEN, padx = 3, pady = 3, borderwidth = 2, width = 500)
        self.txt1 = Entry(self.tbframe, width = 10)
        self.txt2 = Entry(self.tbframe, disabledbackground="#cccccc", width = 10)
        self.btnDesactivar = Button(self.tbframe, text = "Activar/Desactivar")
        self.btnDesactivar.bind('<ButtonRelease-1>', self.btnActivarDesactivar)

        # Lista
        self.lstframe = Frame(frame, relief = SUNKEN, padx = 3, pady = 3, borderwidth = 2, width = 500)
        # Barra de desplazamiento para la lista
        self.VScroll = Scrollbar(self.lstframe)
        self.lista = Listbox(self.lstframe, height = 5, yscrollcommand = self.VScroll.set) # La altura por defecto es 10
        # <<ListboxSelect>> es un evento virtual
        self.lista.bind('<<ListboxSelect>>', self.SeleccionarLista)
        self.VScroll.config(command = self.lista.yview)
        self.btnLimpiarLista = Button(self.lstframe, text = "Limpiar lista", command = self.LimpiarLista, width = 11)
        self.btnRellenarLista = Button(self.lstframe, text = "Rellenar lista", command = self.RellenarLista, width = 11)
        # Rellenamos la lista
        self.RellenarLista()

        # Botones para lanzar mensajes y ventanas de diálogo
        self.mbframe = Frame(frame,relief = SUNKEN,padx = 3, pady = 3, borderwidth = 2)
        self.btnMBInfo = Button(self.mbframe,text = "Info")
        self.btnMBWarning = Button(self.mbframe,text = "Warning")
        self.btnMBError = Button(self.mbframe,text = "Error")
        self.btnMBQuestion = Button(self.mbframe,text = "Question")
        self.btnMBYesNo = Button(self.mbframe,text = "Yes/No")
        self.btnMBInfo.bind('<ButtonRelease-1>', lambda e: self.MostrarMensaje('info'))
        self.btnMBWarning.bind('<ButtonRelease-1>', lambda e: self.MostrarMensaje('warning'))
        self.btnMBError.bind('<ButtonRelease-1>', lambda e: self.MostrarMensaje('error'))
        self.btnMBQuestion.bind('<ButtonRelease-1>', lambda e: self.MostrarMensaje('question'))
        self.btnMBYesNo.bind('<ButtonRelease-1>', lambda e: self.MostrarMensaje('yesno'))
        return frame

    def ColocarWidgets(self, master):
        """Coloca los widgets dentro del frame que los contendrá
        @param master: Frame que contendrá a los widgets
        @type master: Tkinter.Frame"""
        frame = master
        frame.grid(column = 0, row = 0)

        # Colocamos las etiquetas
        self.lblframe.grid(column = 0, row = 1, padx = 5, pady = 5, columnspan = 5,sticky='WE')
        l = Label(self.lblframe,text='Etiquetas |',width=15, anchor='e').grid(column=0,row=0)
        self.lbl1.grid(column = 1, row = 0, padx = 3, pady = 5)
        self.lbl2.grid(column = 2, row = 0, padx = 3, pady = 5)
        self.lbl3.grid(column = 3, row = 0, padx = 3, pady = 5)
        self.lbl4.grid(column = 4, row = 0, padx = 3, pady = 5)
        self.lbl5.grid(column = 5, row = 0, padx = 3, pady = 5)

        # Colocamos los botones
        self.btnframe.grid(column=0, row = 2, padx = 5, pady = 5, columnspan = 5,sticky = 'WE')
        l = Label(self.btnframe,text='Botones |',width=15, anchor='e').grid(column=0,row=0)
        self.btn1.grid(column = 1, row = 0, padx = 3, pady = 3)
        self.btn2.grid(column = 2, row = 0, padx = 3, pady = 3)
        self.btn3.grid(column = 3, row = 0, padx = 3, pady = 3)
        self.btn4.grid(column = 4, row = 0, padx = 3, pady = 3)
        self.btn5.grid(column = 5, row = 0, padx = 3, pady = 3)

        # Colocamos las checkboxes y el botón de conmutación
        self.cbframe.grid(column = 0, row = 3, padx = 5, pady = 5, columnspan = 5,sticky = 'WE')
        l = Label(self.cbframe,text='Checkboxes |',width=15, anchor='e').grid(column=0,row=0)
        self.btnToggleCB.grid(column = 1, row = 0, padx = 3, pady = 3)
        self.chk1.grid(column = 2, row = 0, padx = 3, pady = 3)
        self.chk2.grid(column = 3, row = 0, padx = 3, pady = 3)

        # Colocamos los radiobuttons y seleccionamos el primero
        self.rbframe.grid(column = 0, row = 4, padx = 5, pady = 5, columnspan = 5,sticky = 'WE')
        l = Label(self.rbframe,text='Radiobuttons |',width=15,anchor='e').grid(column=0,row=0)
        self.rb1.grid(column = 2, row = 0, padx = 3, pady = 3, sticky = 'EW')
        self.rb2.grid(column = 3, row = 0, padx = 3, pady = 3, sticky = 'WE')
        self.rb3.grid(column = 4, row = 0, padx = 3, pady = 3, sticky = 'WE')
        self.ValorRadiobuttons1.set("1")
        l = Label(self.rbframe,text='| Otro grupo |',width = 15, anchor = 'e').grid(column = 5, row = 0)
        self.rb4.grid(column = 6, row = 0)
        self.rb5.grid(column = 7, row = 0)
        self.rb6.grid(column = 8, row = 0)
        self.ValorRadiobuttons2.set("1-1")

        # Colocamos las cajas de texto
        self.tbframe.grid(column = 0, row = 5, padx = 5, pady = 5, columnspan = 5,sticky = 'WE')
        l = Label(self.tbframe,text='Cajas de texto |',width=15, anchor='e').grid(column=0,row=0)
        self.txt1.grid(column = 2, row = 0, padx = 3, pady = 3)
        self.txt2.grid(column = 3, row = 0, padx = 3, pady = 3)
        self.btnDesactivar.grid(column = 1, row = 0, padx = 3, pady = 3)

        # Colocamos la lista y sus botones
        self.lstframe.grid(column = 0, row = 6, padx = 5, pady = 5, columnspan = 5,sticky = 'WE')
        l = Label(self.lstframe,text='Lista |',width=15, anchor='e').grid(column=0,row=0,rowspan=2)
        self.lista.grid(column = 2, row = 0,rowspan=2)
        self.VScroll.grid(column = 3, row = 0,rowspan = 2, sticky = 'NSW')
        self.btnLimpiarLista.grid(column = 1, row = 0, padx = 5)
        self.btnRellenarLista.grid(column = 1, row = 1, padx = 5)

        # Colocamos los botones para lanzar mensajes y ventanas de diálogo
        self.mbframe.grid(column = 0,row = 7, columnspan = 5, padx = 5, sticky = 'WE')
        l = Label(self.mbframe,text='Mensajes |',width=15, anchor='e').grid(column=0,row=0)
        self.btnMBInfo.grid(column = 1, row = 0, padx= 3)
        self.btnMBWarning.grid(column = 2, row = 0, padx= 3)
        self.btnMBError.grid(column = 3, row = 0, padx= 3)
        self.btnMBQuestion.grid(column = 4, row = 0, padx= 3)
        self.btnMBYesNo.grid(column = 5, row = 0, padx= 3)

    def BtnCallback(self,valor):
        """Método de callback al pulsar un botón
        @param valor: Determina el tipo de botón pulsado
        @type valor: str"""
        if valor == 'flat':
            print 'Has pulsado el Flat Button...'
        elif valor == 'sunken':
            print 'Has pulsado el Sunken Button...'
        elif valor == 'ridge':
            print 'Has pulsado el Ridge Button...'
        elif valor == 'raised':
            print 'Has pulsado el Raised Button...'
        elif valor == 'groove':
            print 'Has pulsado el Groove Button...'

    def btnConmutar(self,evento):
        """Método de callback del botón "Conmutar".
        Conmuta el valor de las checkboxes.
        @param evento: Evento que provoca la ejecución de este método
        @type evento: Tkinter.Event"""
        self.chk1.toggle()
        self.chk2.toggle()
        print 'La checkbox normal vale %d' % self.ValorCheckbutton1.get()
        print 'La checkbox sin casilla vale %d' % self.ValorCheckbutton2.get()

    def ChkBoxClick(self,valor):
        """Método de callback al pulsar una checkbox
        @param valor: Determina qué checkbox se ha pulsado
        @type valor: int"""
        if valor == 1:
            print 'La checkbox normal vale %d' % self.ValorCheckbutton1.get()
        elif valor == 2:
            print 'La checkbox sin casilla vale %d' % self.ValorCheckbutton2.get()

    def RBClick1(self):
        """Método de callback del grupo 1 de radiobuttons"""
        print 'Seleccionado el radiobutton %d' % self.ValorRadiobuttons1.get()

    def RBClick2(self):
        """Método de callback del grupo 2 de radiobuttons"""
        print 'Seleccionado el radiobutton %s' % self.ValorRadiobuttons2.get()

    def btnActivarDesactivar(self,evento):
        """Método de callback del botón "Activar/Desactivar".
        Activa o desactiva la segunda caja de texto.
        @param evento: Evento que provoca la ejecución de este método
        @type evento: Tkinter.Event"""
        if not self.Desactivado:
            self.Desactivado = True
            self.txt2.configure(state='disabled')
        else:
            self.Desactivado = False
            self.txt2.configure(state='normal')

    def LimpiarLista(self):
        """Método de callback del botón "Limpiar lista".
        Limpia la lista de opciones."""
        self.lista.delete(0,END)

    def RellenarLista(self):
        """Método de callback del botón "Rellenar lista".
        Rellena los elementos de la lista."""
        # OJO: No se hace ninguna comprobación, hay que limpiar la lista antes
        for ejemplo in self.ejemplos:
            self.lista.insert(END,ejemplo)

    def SeleccionarLista(self,evento):
        """Método de callback de la lista de elementos.
        Se activa al seleccionar uno de ellos.
        @param evento: Evento que provoca la ejecución de este método
        @type evento: Tkinter.Event"""
        items = self.lista.curselection()
        seleccionado = items[0]
        print 'Seleccionado el elemento con índice %s y nombre "%s"' % (seleccionado, self.lista.get(seleccionado))

    def MostrarMensaje(self,cual):
        """Método de callback de los botones de mensajes
        @param cual: Indica cuál ha sido el tipo de botón pulsado
        @type cual: str"""
        if cual == 'info':
            tkMessageBox.showinfo('Demo','Ésta es una ventana de INFO')
        elif cual == 'warning':
            tkMessageBox.showwarning('Demo','Ésta es una ventana de WARNING')
        elif cual == 'error':
            tkMessageBox.showerror('Demo','Ésta es una ventana de ERROR')
        elif cual == 'question':
            respuesta = tkMessageBox.askquestion('Demo','¿Ésta es una ventana de QUESTION?')
            print 'Has pulsado %s...' % respuesta
        elif cual == 'yesno':
            respuesta = tkMessageBox.askyesno('Demo','Ésta es una ventana de YES/NO')
            print 'Has pulsado %s...' % respuesta

if __name__ == '__main__':
    raiz = Tk()
    raiz.title('Demo Tkinter')
    raiz.geometry('770x420+350+150')
    demo = Demo(raiz)

    raiz.mainloop()

