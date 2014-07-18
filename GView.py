#!/usr/bin/env python
# -*- coding:utf-8 -*-

# G-View - visor de imágenes ligero para Gnu/Linux #
# Autor: Genesis Vargas J #
# Website: http://www.genesisvargasj.com #
# Licencia: GPL V3 !Software Libre! #

from gi.repository import Gtk, GdkPixbuf, Gdk
from os import system
            
class GView:
	def __init__(self):
		b = Gtk.Builder()
		b.add_from_file("interfaz.glade")
		self.FrmPrincipal = b.get_object("FrmPrincipal")
		self.FrmInfo = b.get_object("FrmInfo")
		self.FrmConfiguracion = b.get_object("FrmConfiguracion")
		self.BtnColor = b.get_object("BtnColor")
		self.CBtnExpandir = b.get_object("CBtnExpandir")
		self.CmbxZoom = b.get_object("CmbxZoom")
		self.BoxImagen = b.get_object("BoxImagen")
		self.BoxHorizontal = b.get_object("eventbox1")
		self.BoxFondoImagen = b.get_object("eventbox2")
		self.CambiarColorFondo(self.BoxFondoImagen, "#FFF")
		self.CambiarColorFondo(self.BoxHorizontal, "#2F6EA9")
		self.CambiarColorFondo(self.FrmPrincipal, "#89A4F1")
		self.image = Gtk.Image()
		self.BoxImagen.add(self.image)
		self.imagenactual = ""
		b.connect_signals(self)
		self.FrmPrincipal.show_all()
		
	def on_BtnSalir_clicked(self, button):
		self.FrmPrincipal.destroy()
		
	def on_BtnAbrirImagen_clicked(self, button):
		dialog = Gtk.FileChooserDialog ("Abrir Imagen", button.get_toplevel(), Gtk.FileChooserAction.OPEN);
		dialog.add_button (Gtk.STOCK_CANCEL, 0)
		dialog.add_button (Gtk.STOCK_OK, 1)
		dialog.set_default_response(1)
		filefilter = Gtk.FileFilter ()
		filefilter.add_pixbuf_formats ()
		dialog.set_filter(filefilter)
		if dialog.run() == 1:
			self.imagenactual = dialog.get_filename()
			self.image.set_from_file(dialog.get_filename())			
		dialog.destroy()
	
	def on_CBtnExpandir_toggled(self, button):
		if self.imagenactual != "":
			if self.CBtnExpandir.get_active():
				self.pixbuf = GdkPixbuf.Pixbuf().new_from_file(self.imagenactual)
				MedidaBox = self.BoxImagen.get_allocation()
				pixbuf = self.pixbuf.scale_simple(MedidaBox.width-10, MedidaBox.height-10, GdkPixbuf.InterpType.BILINEAR)
				self.image.set_from_pixbuf(pixbuf)			
			else:
				self.image.set_from_file(self.imagenactual)	
				
	def on_CmbxZoom_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			zoom = model[tree_iter][0]
			if zoom == "100%":
				self.MostrarZoom(1)
			if zoom == "80%":
				self.MostrarZoom(0.8)
			if zoom == "75%":
				self.MostrarZoom(0.7)
			if zoom == "50%":
				self.MostrarZoom(0.5)
			if zoom == "30%":
				self.MostrarZoom(0.3)		
				
	def on_BtnInfo_clicked(self, button):
		self.FrmInfo.run()
		self.FrmInfo.hide()
		
	def on_BtnCerrarConfiguracion_clicked(self, button):
		self.FrmConfiguracion.hide()
		
	def on_BtnConfiguracion_clicked(self, button):
		self.FrmConfiguracion.run()
		self.FrmConfiguracion.hide()
		
	def on_BtnColor_color_set(self, button):
		self.CambiarColorFondo(self.BoxFondoImagen, self.BtnColor.get_color().to_string())
		
	def on_RbtnLxde_toggled(self, button):
		self.CambiarFondoEscritorio("pcmanfm -w ")	
		
	def on_RbtnXfce_toggled(self, button):
		self.CambiarFondoEscritorio("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s ")	
		
	def on_RbtnGnome_toggled(self, button):
		self.CambiarFondoEscritorio("gsettings set org.gnome.desktop.background picture-uri ")		
		
	def on_RbtnKde_toggled(self, button):
		self.CambiarFondoEscritorio("kwriteconfig --file plasma-appletsrc --group Containments --group 1 --group Wallpaper --group image --key wallpaper ")				
		
	#procedimiento para cambiar el zoom de la imagen dependiendo del numero como parametro recibdo
	def MostrarZoom(self, numero):
		self.pixbuf = GdkPixbuf.Pixbuf().new_from_file(self.imagenactual)
		ancho = int(self.pixbuf.get_width() * numero)
		alto = int(self.pixbuf.get_height() * numero)
		pixbuf = self.pixbuf.scale_simple(ancho, alto, GdkPixbuf.InterpType.BILINEAR)
		self.image.set_from_pixbuf(pixbuf)			
		
	#procedimiento para cambiar el fondo de pantalla utilizando la terminal con el comando que recibe como parametro
	def CambiarFondoEscritorio(self, comando):
		if self.imagenactual != "":
			system(comando + self.imagenactual)
			
	#procedimiento para cambiar color de fondo a window o eventbox con el metodo modify_bg
	def CambiarColorFondo(self, widget, color):
		widget.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(color))
			
GView()
Gtk.main()
