#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ejemplo de uso del módulo PyRTF

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

from PyRTF import *

def rtf_encode(cadena):
    """Codifica una cadena en UTF-8 apta para documentos RTF"""
    resultado = ""
    for caracter in unicode(cadena,'utf-8'):
        resultado = resultado + '\\' + 'u' + str(ord(caracter)) + '?'
    return resultado

def CrearEjemplo():
    """Crea el documento RTF de ejemplo"""
    documento = Document()
    ss = documento.StyleSheet
    seccion = Section()
    documento.Sections.append(seccion)

    # Creamos el estilo "Courier" y lo añadimos a la hoja de estilos
    NormalText = TextStyle(TextPropertySet(ss.Fonts.CourierNew,16))
    estilo = ParagraphStyle('Courier', NormalText.Copy())
    ss.ParagraphStyles.append(estilo)

    # Creamos el estilo "ArialBoldRed" y lo añadimos a la hoja de estilos
    NormalText = TextStyle(TextPropertySet(ss.Fonts.Arial,22,bold=True,colour=ss.Colours.Red))
    estilo = ParagraphStyle('ArialBoldRed', NormalText.Copy())
    ss.ParagraphStyles.append(estilo)

    # Definimos los distintos grosores del borde para su uso posterior
    borde_fino = BorderPS(width=20, style=BorderPS.SINGLE)
    borde_grueso = BorderPS(width=80, style=BorderPS.SINGLE)

    # Definimos los distintos diseños de marco para las tablas para su uso posterior
    marco_fino = FramePS(borde_fino, borde_fino, borde_fino, borde_fino)
    marco_grueso = FramePS(borde_grueso, borde_grueso, borde_grueso, borde_grueso)
    marco_mixto = FramePS(borde_fino, borde_grueso, borde_fino, borde_grueso)

    # Título con estilo "Heading1"
    parrafo = Paragraph(ss.ParagraphStyles.Heading1)
    parrafo.append(rtf_encode('Título 1'))
    seccion.append(parrafo)

    # Párrafo con estilo normal
    parrafo = Paragraph(ss.ParagraphStyles.Normal)
    parrafo.append(rtf_encode('Ésta es la primera prueba de escritura en un documento RTF. '
                   'Este primer párrafo utiliza el estilo predefinido "normal" y todos '
                   'los demás párrafos conservarán este estilo hasta que lo cambiemos.'))
    seccion.append(parrafo)

    # Fuente, tamaño, negrita y cursiva
    parrafo = Paragraph(ss.ParagraphStyles.Normal)
    parrafo.append(rtf_encode('También es posible sobreescribir partes de un estilo concreto: un tamaño de '),
                   TEXT('24 puntos', size=48), ', ',
                   TEXT('fuente Impact', font=ss.Fonts.Impact),
                   rtf_encode(' o más atributos como '),
                   TEXT('negrita', bold=True), ', ',
                   TEXT('cursiva', italic=True), ' o ',
                   TEXT('ambas', bold=True, italic=True), '.')
    seccion.append(parrafo)

    # Fuentes predefinidas en PyRTF
    parrafo = Paragraph()
    parrafo.append(rtf_encode('Éstas son las fuentes predefinidas en PyRTF:'))
    seccion.append(parrafo)
    tabla = Table(TabPS.DEFAULT_WIDTH * 4, TabPS.DEFAULT_WIDTH * 4, TabPS.DEFAULT_WIDTH * 4)
    celda1 = Cell(Paragraph(TEXT('Arial', font=ss.Fonts.Arial)))
    celda2 = Cell(Paragraph(TEXT('CourierNew', font=ss.Fonts.CourierNew)))
    celda3 = Cell(Paragraph(TEXT('MonotypeCorsiva',font=ss.Fonts.MonotypeCorsiva)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('ArialBlack', font=ss.Fonts.ArialBlack)))
    celda2 = Cell(Paragraph(TEXT('FranklinGothicMedium', font=ss.Fonts.FranklinGothicMedium)))
    celda3 = Cell(Paragraph(TEXT('PalatinoLinotype', font=ss.Fonts.PalatinoLinotype)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('ArialNarrow', font=ss.Fonts.ArialNarrow)))
    celda2 = Cell(Paragraph(TEXT('Garamond', font=ss.Fonts.Garamond)))
    celda3 = Cell(Paragraph(TEXT('Papyrus', font=ss.Fonts.Papyrus)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('BitstreamVeraSans', font=ss.Fonts.BitstreamVeraSans)))
    celda2 = Cell(Paragraph(TEXT('Georgia', font=ss.Fonts.Georgia)))
    celda3 = Cell(Paragraph(TEXT('Sylfaen', font=ss.Fonts.Sylfaen)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('BitstreamVeraSerif', font=ss.Fonts.BitstreamVeraSerif)))
    celda2 = Cell(Paragraph(TEXT('Haettenschweiler', font=ss.Fonts.Haettenschweiler)))
    celda3 = Cell(Paragraph(TEXT('Symbol', font=ss.Fonts.Symbol)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('BookAntiqua', font=ss.Fonts.BookAntiqua)))
    celda2 = Cell(Paragraph(TEXT('Impact', font=ss.Fonts.Impact)))
    celda3 = Cell(Paragraph(TEXT('Tahoma', font=ss.Fonts.Tahoma)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('BookmanOldStyle', font=ss.Fonts.BookmanOldStyle)))
    celda2 = Cell(Paragraph(TEXT('LucidaConsole', font=ss.Fonts.LucidaConsole)))
    celda3 = Cell(Paragraph(TEXT('TimesNewRoman', font=ss.Fonts.TimesNewRoman)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('Castellar', font=ss.Fonts.Castellar)))
    celda2 = Cell(Paragraph(TEXT('LucidaSansUnicode', font=ss.Fonts.LucidaSansUnicode)))
    celda3 = Cell(Paragraph(TEXT('TrebuchetMS', font=ss.Fonts.TrebuchetMS)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('CenturyGothic', font=ss.Fonts.CenturyGothic)))
    celda2 = Cell(Paragraph(TEXT('MicrosoftSansSerif', font=ss.Fonts.MicrosoftSansSerif)))
    celda3 = Cell(Paragraph(TEXT('Verdana', font=ss.Fonts.Verdana)))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(TEXT('ComicSansMS',font=ss.Fonts.ComicSansMS)))
    celda2 = Cell(Paragraph())
    celda3 = Cell(Paragraph())
    tabla.AddRow(celda1, celda2, celda3)
    seccion.append(tabla)

    # Colores predefinidos en PyRTF
    parrafo = Paragraph()
    parrafo.append(rtf_encode('Éstos son los colores predefinidos en PyRTF:'))
    seccion.append(parrafo)
    tabla = Table(TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3)
    celda1 = Cell(Paragraph(TEXT('Black', colour=ss.Colours.Black)))
    celda2 = Cell(Paragraph(TEXT('GreenDark',colour=ss.Colours.GreenDark)))
    celda3 = Cell(Paragraph(TEXT('Red',colour=ss.Colours.Red)))
    celda4 = Cell(Paragraph(TEXT('Violet',colour=ss.Colours.Violet)))
    tabla.AddRow(celda1, celda2, celda3, celda4)
    celda1 = Cell(Paragraph(TEXT('Blue',colour=ss.Colours.Blue)))
    celda2 = Cell(Paragraph(TEXT('Grey',colour=ss.Colours.Grey)))
    celda3 = Cell(Paragraph(TEXT('RedDark',colour=ss.Colours.RedDark)))
    celda4 = Cell(Paragraph(TEXT('White',colour=ss.Colours.White)))
    tabla.AddRow(celda1, celda2, celda3, celda4)
    celda1 = Cell(Paragraph(TEXT('BlueDark',colour=ss.Colours.BlueDark)))
    celda2 = Cell(Paragraph(TEXT('GreyDark',colour=ss.Colours.GreyDark)))
    celda3 = Cell(Paragraph(TEXT('Teal',colour=ss.Colours.Teal)))
    celda4 = Cell(Paragraph(TEXT('Yellow',colour=ss.Colours.Yellow)))
    tabla.AddRow(celda1, celda2, celda3, celda4)
    celda1 = Cell(Paragraph(TEXT('Green',colour=ss.Colours.Green)))
    celda2 = Cell(Paragraph(TEXT('Pink',colour=ss.Colours.Pink)))
    celda3 = Cell(Paragraph(TEXT('Turquoise',colour=ss.Colours.Turquoise)))
    celda4 = Cell(Paragraph(TEXT('YellowDark',colour=ss.Colours.YellowDark)))
    tabla.AddRow(celda1, celda2, celda3, celda4)
    seccion.append(tabla)

    # Estilos personalizados
    parrafo = Paragraph(ss.ParagraphStyles.Courier)
    parrafo.append(rtf_encode('Así se ve el estilo personalizado "Courier"'))
    seccion.append(parrafo)

    parrafo = Paragraph(ss.ParagraphStyles.ArialBoldRed)
    parrafo.append(rtf_encode('Así se ve el estilo personalizado "ArialBoldRed"'))
    seccion.append(parrafo)

    # Distintos bordes y estilos para tablas
    tabla = Table(TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3)
    celda1 = Cell(Paragraph(ss.ParagraphStyles.Normal, 'Marco fino'), marco_fino)
    celda2 = Cell(Paragraph('Sin marco'))
    celda3 = Cell(Paragraph('Marco grueso'), marco_grueso)
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(ss.ParagraphStyles.Heading2, rtf_encode('Título 2')))
    celda2 = Cell(Paragraph(ss.ParagraphStyles.Normal, 'Estilo normal'))
    celda3 = Cell(Paragraph(rtf_encode('Más estilo normal')))
    tabla.AddRow(celda1, celda2, celda3)
    celda1 = Cell(Paragraph(ss.ParagraphStyles.Heading2, rtf_encode('Marco mixto')), marco_mixto)
    celda2 = Cell(Paragraph(ss.ParagraphStyles.Normal, 'Sin marco'))
    celda3 = Cell(Paragraph(rtf_encode('Marco mixto')), marco_mixto)
    tabla.AddRow(celda1, celda2, celda3)
    seccion.append(tabla)

    return documento

def AbrirArchivo(nombre):
    """Abre el documento RTF de ejemplo para escribir en él
    @param nombre: Nombre del documento
    @type nombre: str"""
    return file('%s.rtf' % nombre, 'w')

if __name__ == '__main__':
    DR = Renderer()
    documento = CrearEjemplo()
    DR.Write(documento, AbrirArchivo('ejemplo'))
    print 'Hecho'
