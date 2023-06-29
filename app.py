import gi
import sys
import os
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

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.home_dir = os.getenv("HOME")
        self.user_theme_dir = [self.home_dir+"/.themes", self.home_dir+"/.local/share/themes"]
        self.root_theme_dir = ['/usr/share/themes','/usr/local/share/themes']
        self.theme_dir = self.user_theme_dir.extend(self.root_theme_dir) if os.getuid()==0 else self.user_theme_dir
        self.themes = []

        self.set_default_size(400, 300)

        # Create a box layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)

        # Create a list of themes
        theme_list = Gtk.ListBox()
        theme_list.set_vexpand(True)
        theme_list.set_selection_mode(Gtk.SelectionMode.NONE)
        box.append(theme_list)






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