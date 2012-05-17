#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejemplo de uso de colas FIFO, LIFO y de prioridad,
haciendo uso de las bibliotecas Queue y Tkinter

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

from Tkinter import *
import tkMessageBox
import Queue

class EjemploColas:
    """Clase útil para mostrar ejemplos de colas, utilizando
    los widgets básicos de la biblioteca Tkinter."""

    def __init__(self, master = None):
        """Inicializador de la clase EjemploColas
        @param master: Ventana que contendrá el único frame
        @type master: Tkinter.Tk"""
        self.TipoCola = ''
        self.ColaLlena = StringVar()
        self.ColaVacia = StringVar()
        self.ColaVacia.set('Cola vacía')
        self.Item = StringVar()
        self.Salida = StringVar()
        # Definimos las colas
        self.fifo = Queue.Queue(10)
        self.lifo = Queue.LifoQueue(10)
        self.prioridad = Queue.PriorityQueue(10)
        self.cola = self.fifo
        f = self.ConstruirWidgets(master)
        self.ColocarWidgets(f)
        self.MostrarEstado()

    def ConstruirWidgets(self, master):
        """Construye los widgets a mostrar
        @param master: Frame maestro que contendrá al resto
        @type master: Tkinter.Frame
        @return: Frame maestro modificado"""
        frame = Frame(master)
        self.f1 = Frame(frame, relief=SUNKEN, borderwidth=2,
                        width=300, padx=3, pady=3)
        self.btnFifo = Button(self.f1, text="FIFO", state='disabled')
        self.btnFifo.bind('<ButtonRelease-1>',
                          lambda e: self.btnTipoCola('fifo'))
        self.btnLifo = Button(self.f1, text="LIFO", state='active')
        self.btnLifo.bind('<ButtonRelease-1>',
                          lambda e: self.btnTipoCola('lifo'))
        self.btnPrioridad = Button(self.f1, text="PRIORIDAD", state='active')
        self.btnPrioridad.bind('<ButtonRelease-1>',
                               lambda e: self.btnTipoCola('prioridad'))

        self.f2 = Frame(frame, relief=SUNKEN, borderwidth=2,
                        width=300, padx=3, pady=3)
        self.txtEncolar = Entry(self.f2, width=5, textvar=self.Item)
        self.txtEncolar.bind('<Return>', self.Encolar)
        self.txtEncolar.bind('<KP_Enter>', self.Encolar)
        self.btnEncolar = Button(self.f2, text='Encolar', padx=3, pady=3)
        self.btnEncolar.bind('<ButtonRelease-1>', self.Encolar)
        self.btnExtraer = Button(self.f2, text='Extraer',
                             padx=3, pady=3)
        self.btnExtraer.bind('<ButtonRelease-1>', self.Extraer)
        self.lblVacia = Label(self.f2, textvariable=self.ColaVacia,
                              relief=FLAT)
        self.lblLlena = Label(self.f2, textvariable=self.ColaLlena,
                             relief=FLAT)
        self.lblDatos = Label(self.f2, textvariable=self.Salida, relief=FLAT,
                             font=("Helvetica", 16), padx=5)

        return frame

    def ColocarWidgets(self, master):
        """Coloca los widgets dentro del frame que los contendrá
        @param master: Frame que contendrá a los widgets
        @type master: Tkinter.Frame"""
        frame = master
        frame.grid(column=0, row=0)
        l = Label(frame, text='', relief=FLAT, width=15,
                  anchor='e').grid(column=0, row=0)
        l = Label(frame, text='', relief=FLAT, width=15,
                  anchor='e').grid(column=1, row=0)
        l = Label(frame, text='', relief=FLAT, width=15,
                  anchor='e').grid(column=2, row=0)
        l = Label(frame, text='', relief=FLAT, width=15,
                  anchor='e').grid(column=3, row=0)
        l = Label(frame, text='', relief=FLAT, width=15,
                  anchor='e').grid(column=4, row=0)

        self.f1.grid(column=0, row=1, sticky='nsew',
                     columnspan=5, padx=5, pady=5) 
        l = Label(self.f1, text='', width=25,
                  anchor='e').grid(column=0, row=0)
        self.btnFifo.grid(column=1, row=0, padx=4)
        self.btnLifo.grid(column=2, row=0, padx=4)
        self.btnPrioridad.grid(column=3, row=0, padx=4)
        self.f2.grid(column=0, row=2, sticky='nsew',
                     columnspan=5, padx=5, pady=5) 
        l = Label(self.f2,text='', width=15,
                  anchor='e').grid(column=0, row=0)
        self.txtEncolar.grid(column=1, row=0)
        self.btnEncolar.grid(column=2, row=0)
        self.btnExtraer.grid(column=3, row=0)
        self.lblVacia.grid(column=2, row=1)
        self.lblLlena.grid(column=3, row=1)
        self.lblDatos.grid(column=4, row=0)

    def btnTipoCola(self,tipo):
        """Método de callback al pulsar un botón
        @param tipo: Determina el tipo de cola elegida
        @type tipo: str"""
        if tipo == 'fifo' and self.btnFifo.cget('state') == 'active':
            self.TipoCola = 'FIFO'
            self.cola = self.fifo
            raiz.title('Ejemplo de colas - FIFO')
            self.btnFifo.configure(state='disabled')
            self.btnLifo.configure(state='active')
            self.btnPrioridad.configure(state='active')
            print self.TipoCola
        elif tipo == 'lifo' and self.btnLifo.cget('state') == 'active':
            self.TipoCola = 'LIFO'
            self.cola = self.lifo
            raiz.title('Ejemplo de colas - LIFO')
            self.btnFifo.configure(state='active')
            self.btnLifo.configure(state='disabled')
            self.btnPrioridad.configure(state='active')
            print self.TipoCola
        elif tipo == 'prioridad' and self.btnPrioridad.cget('state') == 'active':
            self.TipoCola = 'PRIORIDAD'
            self.cola = self.prioridad
            raiz.title('Ejemplo de colas - Prioridad')
            self.btnFifo.configure(state='active')
            self.btnLifo.configure(state='active')
            self.btnPrioridad.configure(state='disabled')
            print self.TipoCola
        elif tipo == 'ring':
            self.TipoCola = 'RING'
        self.MostrarEstado()

    def MostrarEstado(self):
        """Muestra el estado actual de la cola (si está vacía o llena)"""
        # Comprobamos si la cola está vacía
        if self.cola.empty() == True:
            self.ColaVacia.set('Cola vacía')
        else:
            self.ColaVacia.set('')
        # Comprobamos si la cola está llena
        if self.cola.full() == True:
            self.ColaLlena.set('COLA LLENA')
        else:
            self.ColaLlena.set('')

    def Encolar(self, evento):
        """Método de callback del botón "Encolar".
        Encola el elemento introducido mediante la caja de texto.
        @param evento: Evento que provoca la ejecución de este método
        @type evento: Tkinter.Event"""
        elemento = self.Item.get()
        if self.TipoCola == 'PRIORIDAD':
            if elemento.find(',') == -1:
                print 'ERROR'
                tkMessageBox.showerror('Ejemplo de colas', 'En una cola de '
                'prioridad las entradas tienen el formato\r(prioridad, dato)')
            else:
                self.cola.put(self.Item.get())
        elif not self.cola.full():
            self.cola.put(self.Item.get())
        self.Item.set('')
        self.MostrarEstado()

    def Extraer(self, evento):
        """Método de callback del botón "Extraer".
        Extrae un elemento de la cola.
        @param evento: Evento que provoca la ejecución de este método
        @type evento: Tkinter.Event"""
        self.Salida.set('')
        if not self.cola.empty():
            elemento = self.cola.get()
            self.Salida.set("Sacamos \"%s\"" % elemento)
        self.MostrarEstado()

if __name__ == '__main__':

    def Center(ventana):
        """Centra una ventana
        @param ventana: Ventana a centrar
        @type ventana: Tkinter.Tk"""
        print ventana
        # Ancho y alto de la pantalla
        sw = ventana.winfo_screenwidth()
        sh = ventana.winfo_screenheight()
        # Ancho y alto de la ventana
        rw = ventana.winfo_reqwidth()
        rh = ventana.winfo_reqheight()
        xc = (sw-rw)/2
        yc = (sh-rh)/2
        ventana.geometry("%dx%d+%d+%d"%(rw,rh,xc,yc))
        ventana.deiconify()

    raiz = Tk()
    raiz.title('Ejemplo de colas - FIFO')
    demo = EjemploColas(raiz)   
    raiz.after(3,Center,raiz)
    raiz.mainloop()
