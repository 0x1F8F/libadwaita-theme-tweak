#!/bin/python3
import gi
import sys
import os
import shutil
gi.require_version('Gtk','4.0')

from gi.repository import Gtk,GLib

def themes(theme_dir):
    themes = []
    for dir in theme_dir:
        for theme in os.listdir(dir):
            if os.path.isdir(theme):
                themes.append(theme)
    return themes


class MainWindow(Gtk.ApplicationWindow):
    def __themes__(self):
        for dir in self.theme_dir:
            for theme in os.listdir(dir):
                if os.path.isdir(theme):
                    self.themes.append(theme)

    def on_apply_clicked(self,button, theme):
        print(f"Apply button clicked for theme: {theme}")
        if os.path.isdir(self.home_dir+'/.config/gtk-4.0'):
            shutil.rmtree(self.home_dir+'/.config/gtk-4.0')
        shutil.copytree(theme+'/gtk-4.0/',self.home_dir+'/.config/gtk-4.0')
        print("Progress succeeded GTK 4.0")
        if os.path.isdir(self.home_dir+'/.config/gtk-3.0'):
            shutil.rmtree(self.home_dir+'/.config/gtk-3.0')
        shutil.copytree(theme+'/gtk-3.0/',self.home_dir+'/.config/gtk-3.0')
        print("Progress succeeded GTK 3.0")


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.home_dir = os.getenv("HOME")
        self.user_theme_dir = [self.home_dir+"/.themes", self.home_dir+"/.local/share/themes"]
        self.root_theme_dir = ['/usr/share/themes','/usr/local/share/themes']
        self.theme_dir = self.user_theme_dir+self.root_theme_dir if os.getuid()==0 else self.user_theme_dir
        self.themes = []
        print("THEME DIR: ",self.theme_dir)

        for dir in self.theme_dir:
            try:
                for theme in os.listdir(dir):
                    if os.path.isdir(dir+'/'+theme):
                        self.themes.append(dir+'/'+theme)
            except Exception as err:
                print(f"CRITICAL : {err}")

        print(self.themes,self.theme_dir)
        self.set_default_size(800, 500)

        # Create a box layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        box.append(scrolled_window)

        listbox = Gtk.ListBox()
        scrolled_window.set_child(listbox)

        # Create and add list items
        for i in self.themes:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            title = Gtk.Label(label=f"{i.split('/')[-1]}")
            title.set_hexpand(True)
            box.append(title)
            apply_btn = Gtk.Button(label=f"Apply")
            apply_btn.connect("clicked",self.on_apply_clicked,i)
            apply_btn.set_margin_end(8)
            box.append(apply_btn)
            box.set_margin_top(4)
            box.set_margin_bottom(4)
            listbox.append(box)





class Application(Gtk.Application):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.win = None
        self.connect("activate",self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = Application()
sys.exit(app.run(sys.argv))