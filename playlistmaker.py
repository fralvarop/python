#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de creación de listas de reproducción.
@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

import sys
import os.path
from mutagen.mp3 import MP3

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

__docformat__ = "epytext"

class PlayListCreator:
    """Clase que permite crear una lista de reproducción
    de archivos MP3 en formato .m3u8"""

    def __init__(self):
        """Inicializador de la clase PlayListCreator"""
        self.gladefile = "playlistmaker.glade"
        self.wTree = gtk.glade.XML(self.gladefile,"MainWindow")
        self.SetEventDictionary()
        self.SetWidgetReferences()
        self.SetupToolTips()
        self.DisableScrollButtons()
        self.tbtnDelete.set_sensitive(False)
        self.tbtnClearAll.set_sensitive(False)
        self.SetupTreeview()
        self.CurrentPath = ""
        self.CurrentRow = 0
        self.RowCount = 0

    def SetEventDictionary(self):
        """Establece el diccionario que asocia un método a cada evento"""
        dict = {"on_MainWindow_destroy": gtk.main_quit,
                "on_tbtnQuit_clicked": gtk.main_quit,
                "on_tbtnAdd_clicked": self.on_tbtnAdd_clicked,
                "on_tbtnDelete_clicked": self.on_tbtnDelete_clicked,
                "on_tbtnClearAll_clicked": self.on_tbtnClearAll_clicked,
                "on_tbtnMoveToTop_clicked": self.on_tbtnMoveToTop_clicked,
                "on_tbtnMoveUp_clicked": self.on_tbtnMoveUp_clicked,
                "on_tbtnMoveDown_clicked": self.on_tbtnMoveDown_clicked,
                "on_tbtnMoveToBottom_clicked": self.on_tbtnMoveToBottom_clicked,
                "on_tbtnAbout_clicked": self.on_tbtnAbout_clicked,
                "on_btnGetFolder_clicked": self.on_btnGetFolder_clicked,
                "on_txtFilename_key_press_event": self.txtFilenameKeyPress,
                "on_btnSavePlaylist_clicked": self.on_btnSavePlaylist_clicked}
        self.wTree.signal_autoconnect(dict)

    def SetWidgetReferences(self):
        """Referencia los widgets definidos en el fichero .glade"""
        self.txtFilename = self.wTree.get_widget("txtFilename")
        self.txtPath = self.wTree.get_widget("txtPath")
        self.tbtnAdd = self.wTree.get_widget("tbtnAdd")
        self.tbtnDelete = self.wTree.get_widget("tbtnDelete")
        self.tbtnClearAll = self.wTree.get_widget("tbtnClearAll")
        self.tbtnQuit = self.wTree.get_widget("tbtnQuit")
        self.tbtnAbout = self.wTree.get_widget("tbtnAbout")
        self.tbtnMoveToTop = self.wTree.get_widget("tbtnMoveToTop")
        self.tbtnMoveUp = self.wTree.get_widget("tbtnMoveUp")
        self.tbtnMoveDown = self.wTree.get_widget("tbtnMoveDown")
        self.tbtnMoveToBottom = self.wTree.get_widget("tbtnMoveToBottom")
        self.btnGetFolder = self.wTree.get_widget("btnGetFolder")
        self.btnSavePlaylist = self.wTree.get_widget("btnSavePlaylist")
        self.sbar = self.wTree.get_widget("statusbar1")
        self.context_id = self.sbar.get_context_id("Statusbar")

    def SetupToolTips(self):
        """Establece el texto de ayuda de cada botón
        cuando el usuario pasa el ratón por encima"""
        self.tbtnAdd.set_tooltip_text("Añadir uno o más archivos a la lista de reproducción")
        self.tbtnAbout.set_tooltip_text("Acerca de...")
        self.tbtnDelete.set_tooltip_text("Eliminar la entrada seleccionada de la lista de reproducción")
        self.tbtnClearAll.set_tooltip_text("Limpiar la lista")
        self.tbtnQuit.set_tooltip_text("Cerrar este programa")
        self.tbtnMoveToTop.set_tooltip_text("Mover la entrada seleccionada al inicio de la lista de reproducción")
        self.tbtnMoveUp.set_tooltip_text("Mover hacia arriba la entrada seleccionada")
        self.tbtnMoveDown.set_tooltip_text("Mover hacia abajo la entrada seleccionada")
        self.tbtnMoveToBottom.set_tooltip_text("Mover la entrada seleccionada al final de la lista de reproducción")
        self.btnGetFolder.set_tooltip_text("Elegir la carpeta donde se guardará la lista de reproducción")
        self.btnSavePlaylist.set_tooltip_text("Guardar la lista de reproducción")
        self.txtFilename.set_tooltip_text("Nombre para la lista de reproducción. La extensión '.m3u' se añadirá automáticamente")

    def EnableScrollButtons(self):
        """Habilita los botones de desplazamiento
        de elementos a lo largo de la lista"""
        self.tbtnMoveToTop.set_sensitive(True)
        self.tbtnMoveUp.set_sensitive(True)
        self.tbtnMoveDown.set_sensitive(True)
        self.tbtnMoveToBottom.set_sensitive(True)

    def DisableScrollButtons(self):
        """Deshabilita los botones de desplazamiento
        de elementos a lo largo de la lista"""
        self.tbtnMoveToTop.set_sensitive(False)
        self.tbtnMoveUp.set_sensitive(False)
        self.tbtnMoveDown.set_sensitive(False)
        self.tbtnMoveToBottom.set_sensitive(False)

    def SetupTreeview(self):
        """Configura el treeview"""
        self.cFName = 0
        self.cFType = 1
        self.cFPath = 2
        self.sFName = "Nombre"
        self.sFType = "Tipo"
        self.sFPath = "Carpeta"
        self.treeview = self.wTree.get_widget("treeview1")
        self.AddPlaylistColumn(self.sFName,self.cFName)
        self.AddPlaylistColumn(self.sFType,self.cFType)
        self.AddPlaylistColumn(self.sFPath,self.cFPath)
        self.playList = gtk.ListStore(str,str,str)
        self.treeview.set_model(self.playList)
        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    def AddPlaylistColumn(self,title,columnId):
        """Añade una columna al editor de la lista de reproducción
        @param title: Título de la columna
        @type title: str
        @param columnId: Identificador de la columna
        @type columnId: int"""
        column = gtk.TreeViewColumn(title,gtk.CellRendererText(),text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.treeview.append_column(column)

    def on_tbtnAdd_clicked(self,widget):
        """Método de callback del botón \"Añadir\"\n
        Añade los archivos MP3 seleccionados a la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        fd = FileDialog()
        selectedfiles,self.CurrentPath = fd.ShowFileChooserDialog(self.CurrentPath)
        counter = 0
        for f in selectedfiles:
            extStart = f.rfind(".")
            fnameStart = f.rfind("/")
            extension = f[extStart+1:]
            fname = f[fnameStart+1:extStart]
            fpath = f[:fnameStart]
            data = [fname,extension,fpath]
            self.playList.append(data)
            counter += 1
        self.RowCount += counter
        if self.RowCount > 0:
            self.tbtnDelete.set_sensitive(True)
            self.tbtnClearAll.set_sensitive(True)
            if self.RowCount > 1:
                self.EnableScrollButtons()
        self.sbar.push(self.context_id,"%s archivos añadidos de un total de %d" % (counter,self.RowCount))

    def on_tbtnDelete_clicked(self,widget):
        """Método de callback del botón \"Quitar\"\n
        Elimina los archivos MP3 seleccionados de la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        sel = self.treeview.get_selection()
        (model,rows) = sel.get_selected_rows()
        iters=[]
        for row in rows:
            iters.append(self.playList.get_iter(row))
        for i in iters:
            if i is not None:
                self.playList.remove(i)
                self.RowCount -= 1
        if self.RowCount < 2:
            self.DisableScrollButtons()
            if self.RowCount == 0:
                self.tbtnDelete.set_sensitive(False)
                self.tbtnClearAll.set_sensitive(False)
        self.sbar.push(self.context_id,"%d archivos en la lista" % (self.RowCount))

    def on_tbtnClearAll_clicked(self,widget):
        """Método de callback del botón \"Limpiar\"\n
        Vacía la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        self.DisableScrollButtons()
        self.tbtnDelete.set_sensitive(False)
        self.tbtnClearAll.set_sensitive(False)
        self.playList.clear()
        self.sbar.push(self.context_id,"Lista vacía")

    def on_tbtnMoveToTop_clicked(self,widget):
        """Método de callback del botón \"Principio\"\n
        Mueve el archivo MP3 seleccionado al principio de la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        sel = self.treeview.get_selection()
        (model,rows) = sel.get_selected_rows()
        for path1 in rows:
            path2 = 0
        iter1 = model.get_iter(path1)
        iter2 = model.get_iter(path2)
        model.move_before(iter1,iter2)

    def on_tbtnMoveUp_clicked(self,widget):
        """Método de callback del botón \"Arriba\"\n
        Mueve el archivo MP3 seleccionado una posición más arriba en la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        sel = self.treeview.get_selection()
        (model,rows) = sel.get_selected_rows()
        for path1 in rows:
            path2 = (path1[0]-1,)
        if path2[0] >= 0:
            iter1=model.get_iter(path1)
            iter2 = model.get_iter(path2)
            model.swap(iter1,iter2)

    def on_tbtnMoveDown_clicked(self,widget):
        """Método de callback del botón \"Abajo\"\n
        Mueve el archivo MP3 seleccionado una posición más abajo en la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        sel = self.treeview.get_selection()
        (model,rows) = sel.get_selected_rows()
        for path1 in rows:
            path2 = (path1[0]+1,)
        iter1=model.get_iter(path1)
        if path2[0] <= self.RowCount-1:
            iter2 = model.get_iter(path2)
            model.swap(iter1,iter2)

    def on_tbtnMoveToBottom_clicked(self,widget):
        """Método de callback del botón \"Final\"\n
        Mueve el archivo MP3 seleccionado al final de la lista de reproducción
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        sel = self.treeview.get_selection()
        (model,rows) = sel.get_selected_rows()
        for path1 in rows:
            path2 = self.RowCount-1
        iter1=model.get_iter(path1)
        iter2 = model.get_iter(path2)
        model.move_after(iter1,iter2)

    def on_tbtnAbout_clicked(self,widget):
        """Método de callback del botón \"Acerca de...\"\n
        Muestra en un cuadro de diálogo información básica sobre el programa
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.ToolButton"""
        about = gtk.AboutDialog()
        about.set_program_name("Playlist Maker")
        about.set_version("1.0")
        about.set_copyright("(c) 2011 by Greg Walters")
        about.set_comments("Written for Full Circle Magazine")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("logo.png"))
        about.set_icon(gtk.gdk.pixbuf_new_from_file("logo.png"))
        about.set_website("http://thedesignatedgeek.com")
        about.run()
        about.destroy()

    def on_btnGetFolder_clicked(self,widget):
        """Método de callback del botón \"Carpeta...\"\n
        Permite al usuario elegir la carpeta donde se guardará la lista mediante cuadros de diálogo
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.Button"""
        fd = FileDialog()
        filepath,self.CurrentPath = fd.ShowFolderChooserDialog(self.CurrentPath)
        if len(filepath) == 1:
            self.txtPath.set_text(filepath[0])

    def txtFilenameKeyPress(self,widget,data):
        """Método de callback del campo de texto \"Nombre de fichero:\"\n
        Si el usuario pulsa la tecla intro, procedemos a guardar la lista
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: Gtk.Entry
        @param data: Tecla pulsada
        @type data: gtk.gdk.Event"""
        if data.keyval == 65293: # Ante un intro, procedemos a guardar la lista
            self.SavePlaylist()

    def on_btnSavePlaylist_clicked(self,widget):
        """Método de callback del botón \"Guardar\"
        @param widget: Widget que ha provocado la ejecución de este método tras un evento
        @type widget: gtk.Button"""
        self.SavePlaylist()

    def SavePlaylist(self):
        """Guarda la lista de reproducción"""
        # Leemos la ruta del campo de texto correspondiente
        filepath = self.txtPath.get_text()
        # Leemos el nombre para la lista del campo de texto correspondiente
        filename = self.txtFilename.get_text()

        if filepath == "":
            self.MessageBox("error","Por favor, indica una ruta para la lista de reproducción.")
        elif filename == "":
            self.MessageBox("error","Por favor, indica un nombre para la lista de reproducción.")
        else:
            extStart = filename.rfind(".") # Buscamos la extensión
            if extStart == -1:
                filename += '.m3u' # Añadimos la extensión si no la tenía
                self.txtFilename.set_text(filename) # Actualizamos el nombre en el campo de texto
            if os.path.exists(filepath + "/" + filename):
                self.MessageBox("error","El archivo ya existe. Por favor elige otro.")
            else:
                plfile = open(filepath + "/" + filename,"w")  # Abrimos el fichero
                plfile.writelines('#EXTM3U\n')  # Añadimos la cabecera M3U
                for row in self.playList:
                    fname = "%s/%s.%s" % (row[2],row[0],row[1])
                    artist,title,songlength = self.GetMP3Info(fname)
                    if songlength > 0 and (artist != '' and title != ''):
                        plfile.writelines("#EXTINF:%d,%s - %s\n" % (songlength,artist,title))
                    plfile.writelines("%s\n" % fname)
                plfile.close  # Cerramos el fichero
                self.MessageBox("info","¡Lista de reproducción guardada!")

    def GetMP3Info(self,filename):
        """Lee la etiqueta ID3 de un archivo MP3
        @param filename: Nombre del archivo MP3 a examinar
        @type filename: str
        @return: Tupla con el nombre del artista, título y duración"""
        artist = ''
        title = ''
        songlength = 0
        audio = MP3(filename)
        keys = audio.keys()
        for key in keys:
            try:
                if key == "TPE1":             # Artista
                    artist = audio.get(key)
            except:
                artist = ''
            try:
                if key == "TIT2":             # Título
                    title = audio.get(key)
            except:
                title = ''
            songlength = audio.info.length    # Duración
        return (artist,title,songlength)

    def MessageBox(self,level,text):
        """Muestra un cuadro de diálogo con el texto y el tipo indicados
        @param level: Tipo de cuadro de diálogo: notificación, advertencia, error o pregunta)
        @type level: str
        @param text: Texto a mostrar en el cuadro de diálogo
        @type text: str
        @return: Si es una pregunta, el resultado de la ejecución del cuadro de diálogo: sí/no"""
        if level == "info":
            dlg = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,text)
        elif level == "warning":
            dlg = gtk.MessageDialog(None,0,gtk.MESSAGE_WARNING,gtk.BUTTONS_OK,text)
        elif level == "error":
            dlg = gtk.MessageDialog(None,0,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,text)
        elif level == "question":
            dlg = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,text)
        if level == "question":
            resp = dlg.run()
            dlg.destroy()
            return resp
        else:
            resp = dlg.run()
            dlg.destroy()

class FileDialog:
    """Cuadro de diálogo para seleccionar uno o más archivos o directorios"""

    def ShowFileChooserDialog(self,CurrentPath):
        """Muestra un cuadro de diálogo para seleccionar uno o más archivos
        @param CurrentPath: Ruta actual
        @type CurrentPath: str
        @return: Tupla con dos elementos: la lista de los archivos seleccionados y la ruta actual"""
        #gtk.FileChooserDialog(title,parent,action,buttons,backend)
        dialog = gtk.FileChooserDialog("Elige archivos a añadir...", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        filter = gtk.FileFilter()
        filter.set_name("Archivos de música")
        filter.add_pattern("*.mp3")
        filter.add_pattern("*.ogg")
        filter.add_pattern("*.wav")
        dialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Todos los archivos")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_select_multiple(True)

        if CurrentPath != "":
            dialog.set_current_folder(CurrentPath)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            fileselection = dialog.get_filenames()
            CurrentPath = dialog.get_current_folder()
            dialog.destroy()
            return (fileselection,CurrentPath)
        elif response == gtk.RESPONSE_CANCEL:
            dialog.destroy()
            return ([],"")

    def ShowFolderChooserDialog(self,CurrentPath):
        """Muestra un cuadro de diálogo para elegir un directorio
        @param CurrentPath: Ruta actual
        @type CurrentPath: str
        @return: Tupla con dos elementos: el directorio seleccionado y la ruta actual"""
        #gtk.FileChooserDialog(title,parent,action,buttons,backend)
        dialog = gtk.FileChooserDialog("Elige carpeta destino...", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

        if CurrentPath != "":
            dialog.set_current_folder(CurrentPath)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            fileselection = dialog.get_filenames()
            CurrentPath = dialog.get_current_folder()
            dialog.destroy()
            return (fileselection,CurrentPath)
        elif response == gtk.RESPONSE_CANCEL:
            dialog.destroy()
            return ([],"")

if __name__ == "__main__":
    plc = PlayListCreator()
    gtk.main()

