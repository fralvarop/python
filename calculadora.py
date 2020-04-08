#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculadora sencilla que implementa las cuatro reglas,
con números positivos y negativos con o sin decimales.

Ejemplo de uso de la biblioteca Tkinter
@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

from Tkinter import *

__docformat__ = "epytext"

class Calculadora():
    """Clase que implementa una calculadora sencilla, con
    soporte para las cuatro reglas, con números positivos
    y negativos con o sin decimales."""

    def __init__(self,raiz):
        """Inicializador de la clase Calculadora
        @param raiz: Ventana que contendrá el único frame
        @type raiz: Tkinter.Tk"""
        master = Frame(raiz)
        self.ValorActual = 0
        self.ValorGuardado = 0
        self.OperacionActual = ''
        self.Pantalla = StringVar()
        self.Pantalla.set('0')
        self.Positivo = True
        self.SiguienteDecimal = False
        self.Decimales = 0
        self.DefinirWidgets(master)
        self.ColocarWidgets(master)

    def DefinirWidgets(self,master):
        """Define los widgets a mostrar en la calculadora
        @param master: Frame que contendrá a los widgets
        @type master: Tkinter.Frame"""
        self.lblPantalla = Label(master, anchor=E, relief=SUNKEN, bg="white", height=2, textvariable=self.Pantalla)
        self.btn1 = Button(master, text = '1', width = 4, height = 3)
        self.btn1.bind('<ButtonRelease-1>', lambda e: self.funcNumero(1))
        self.btn2 = Button(master, text = '2', width = 4, height = 3)
        self.btn2.bind('<ButtonRelease-1>', lambda e: self.funcNumero(2))
        self.btn3 = Button(master, text = '3', width = 4, height = 3)
        self.btn3.bind('<ButtonRelease-1>', lambda e: self.funcNumero(3))
        self.btn4 = Button(master, text = '4', width = 4, height = 3)
        self.btn4.bind('<ButtonRelease-1>', lambda e: self.funcNumero(4))
        self.btn5 = Button(master, text = '5', width = 4, height = 3)
        self.btn5.bind('<ButtonRelease-1>', lambda e: self.funcNumero(5))
        self.btn6 = Button(master, text = '6', width = 4, height = 3)
        self.btn6.bind('<ButtonRelease-1>', lambda e: self.funcNumero(6))
        self.btn7 = Button(master, text = '7', width = 4, height = 3)
        self.btn7.bind('<ButtonRelease-1>', lambda e: self.funcNumero(7))
        self.btn8 = Button(master, text = '8', width = 4, height = 3)
        self.btn8.bind('<ButtonRelease-1>', lambda e: self.funcNumero(8))
        self.btn9 = Button(master, text = '9', width = 4, height = 3)
        self.btn9.bind('<ButtonRelease-1>', lambda e: self.funcNumero(9))
        self.btn0 = Button(master, text = '0', width = 4, height = 3)
        self.btn0.bind('<ButtonRelease-1>', lambda e: self.funcNumero(0))
        self.btnGuion = Button(master, text = '-', width = 4, height = 3)
        self.btnGuion.bind('<ButtonRelease-1>', lambda e: self.funcOperador('CambioSigno'))
        self.btnPunto = Button(master, text = '.', width = 4, height = 3)
        self.btnPunto.bind('<ButtonRelease-1>', lambda e: self.funcOperador('Decimal'))
        self.btnMas = Button(master,text = '+', width = 4, height = 3)
        self.btnMas.bind('<ButtonRelease-1>', lambda e: self.funcOperador('Sumar'))
        self.btnMenos = Button(master,text = '-', width = 4, height = 3)
        self.btnMenos.bind('<ButtonRelease-1>', lambda e: self.funcOperador('Restar'))
        self.btnPor = Button(master,text = '*', width = 4, height = 3)
        self.btnPor.bind('<ButtonRelease-1>', lambda e: self.funcOperador('Multiplicar'))
        self.btnEntre = Button(master,text = '/', width = 4, height = 3)
        self.btnEntre.bind('<ButtonRelease-1>', lambda e: self.funcOperador('Dividir'))
        self.btnIgual = Button(master, text = '=', width = 4, height = 3)
        self.btnIgual.bind('<ButtonRelease-1>', lambda e: self.funcOperador('Igual'))
        self.btnBorrar = Button(master, text = 'C', width = 4, height = 3)
        self.btnBorrar.bind('<ButtonRelease-1>', lambda e: self.funcBorrar())

    def ColocarWidgets(self,master):
        """Coloca los widgets dentro del frame que los contendrá
        @param master: Frame que contendrá a los widgets
        @type master: Tkinter.Frame"""
        master.grid(column=0, row=0)
        self.lblPantalla.grid(column=0, row=0, columnspan = 4, sticky=EW)
        self.btn1.grid(column = 0, row = 1)
        self.btn2.grid(column = 1, row = 1)
        self.btn3.grid(column = 2, row = 1)
        self.btn4.grid(column = 0, row = 2)
        self.btn5.grid(column = 1, row = 2)
        self.btn6.grid(column = 2, row = 2)
        self.btn7.grid(column = 0, row = 3)
        self.btn8.grid(column = 1, row = 3)
        self.btn9.grid(column = 2, row = 3)
        self.btn0.grid(column = 1, row = 4)
        self.btnGuion.grid(column = 0, row = 4)
        self.btnPunto.grid(column = 2, row = 4)
        self.btnMas.grid(column = 3, row = 1)
        self.btnMenos.grid(column = 3, row = 2)
        self.btnPor.grid(column = 3, row = 3)
        self.btnEntre.grid(column=3, row = 4)
        self.btnIgual.grid(column=0, row=5, columnspan = 3, sticky = NSEW)
        self.btnBorrar.grid(column=3, row=5, columnspan = 1, sticky = NSEW)

    def funcNumero(self,valor):
        """Método de callback al pulsar el botón de un número
        @param valor: Valor del número introducido
        @type valor: int"""
        if self.Positivo:
            if self.SiguienteDecimal:
                self.Decimales += 1
                self.ValorActual = self.ValorActual + (valor * (10**-self.Decimales))
            else:
                self.ValorActual = (self.ValorActual * 10) + valor
        else:
            if self.SiguienteDecimal:
                self.Decimales += 1
                self.ValorActual = self.ValorActual - (valor * (10**-self.Decimales))
            else:
                self.ValorActual = (self.ValorActual * 10) - valor
        self.Mostrar()

    def funcBorrar(self):
        """Limpia la pantalla de la calculadora, así como las variables temporales"""
        self.ValorActual = 0
        self.ValorGuardado = 0
        self.Positivo = True
        self.SiguienteDecimal = False
        self.Decimales = 0
        self.Mostrar()

    def funcOperador(self,operacion):
        """Método de callback al pulsar el botón de un operador
        @param operacion: Operación a realizar
        @type operacion: str"""
        if operacion == 'Decimal':
            self.SiguienteDecimal = True
        else:
            if operacion == 'CambioSigno':
                self.Positivo = not self.Positivo
                self.ValorActual *= -1
                self.Mostrar()
            elif operacion == 'Sumar':
                self.ValorGuardado = self.ValorActual
                self.ValorActual = 0
                self.Positivo = True
                self.SiguienteDecimal = False
                self.Decimales = 0
                self.OperacionActual = 'Sumar'
            elif operacion == 'Restar':
                self.ValorGuardado = self.ValorActual
                self.ValorActual = 0
                self.Positivo = True
                self.SiguienteDecimal = False
                self.Decimales = 0
                self.OperacionActual = 'Restar'
            elif operacion == 'Multiplicar':
                self.ValorGuardado = self.ValorActual
                self.ValorActual = 0
                self.Positivo = True
                self.SiguienteDecimal = False
                self.Decimales = 0
                self.OperacionActual = 'Multiplicar'
            elif operacion == 'Dividir':
                self.ValorGuardado = self.ValorActual
                self.ValorActual = 0
                self.Positivo = True
                self.SiguienteDecimal = False
                self.Decimales = 0
                self.OperacionActual = 'Dividir'
            elif operacion == 'Igual':
                if self.OperacionActual == 'Sumar':
                    self.ValorActual += self.ValorGuardado
                elif self.OperacionActual == 'Restar':
                    self.ValorActual = self.ValorGuardado - self.ValorActual
                elif self.OperacionActual == 'Multiplicar':
                    self.ValorActual *= self.ValorGuardado
                elif self.OperacionActual == 'Dividir':
                    self.ValorActual = self.ValorGuardado / self.ValorActual
                self.Mostrar()
                self.ValorActual = 0
                self.ValorGuardado = 0
                self.Positivo = True
                self.SiguienteDecimal = False
                self.Decimales = 0

    def Mostrar(self):
        """Refresca la pantalla de la calculadora"""
        self.Pantalla.set(self.ValorActual)

if __name__ == '__main__':
    global val, calculadora, raiz
    raiz = Tk()
    raiz.title('Calculadora sencilla')
    raiz.geometry('247x330+469+199')
    calculadora = Calculadora(raiz)
    raiz.mainloop()

