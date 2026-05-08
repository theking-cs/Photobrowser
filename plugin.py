from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap
from enigma import ePicLoad, ePoint, eSize, getDesktop
from Plugins.Plugin import PluginDescriptor
import os
from PIL import Image

# Resolución pantalla
dw = getDesktop(0).size().width()
dh = getDesktop(0).size().height()

# -------------------------------------------------------
# EXPLORADOR DE FOTOS (NAVEGACIÓN TOTAL)
# -------------------------------------------------------
class PhotoBrowserScreen(Screen):
    skin = """
    <screen name="PhotoBrowser" position="center,center" size="1200,720" title="Photo Browser Gallery" backgroundColor="#101010" flags="wfNoBorder">
        <eLabel position="0,0" size="380,720" backgroundColor="#1a1a1a" zPosition="-1" />
        
        <!-- Firma by Zoubair91 en ROJO -->
        <widget name="by_author" position="800,20" size="380,30" font="Regular;22" halign="right" foregroundColor="#ff0000" transparent="1" zPosition="2" />
        
        <widget name="filelist" position="20,80" size="340,540" itemHeight="45" scrollbarMode="showOnDemand" transparent="1" />
        <widget name="status" position="20,20" size="340,50" font="Regular;18" foregroundColor="#00ff00" transparent="1" />
        <eLabel position="380,0" size="820,720" backgroundColor="#000000" zPosition="-1" />
        <widget name="preview" position="400,60" size="780,600" alphatest="blend" zPosition="1" />
        
        <!-- Botonera Inferior -->
        <ePixmap pixmap="buttons/red.png" position="20,670" size="35,25" alphatest="on" />
        <widget name="key_red" position="60,670" size="80,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" />
        
        <ePixmap pixmap="buttons/green.png" position="150,670" size="35,25" alphatest="on" />
        <widget name="key_green" position="190,670" size="80,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" />

        <ePixmap pixmap="buttons/yellow.png" position="280,670" size="35,25" alphatest="on" />
        <widget name="key_yellow" position="320,670" size="80,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" />

        <ePixmap pixmap="buttons/blue.png" position="410,670" size="35,25" alphatest="on" />
        <widget name="key_blue" position="450,670" size="80,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" />

        <widget name="info" position="600,670" size="580,30" font="Regular;18" halign="right" foregroundColor="#888888" transparent="1" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self["filelist"] = MenuList([])
        self["preview"] = Pixmap()
        self["status"] = Label("")
        
        # Firma del autor
        self["by_author"] = Label("by Zoubair91")
        
        self["key_red"] = Label("ROTATE")
        self["key_green"] = Label("EXIT")
        self["key_yellow"] = Label("ZOOM +")
        self["key_blue"] = Label("ZOOM -")
        self["info"] = Label("OK: Fullscreen | 1: Rotate")

        self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "NumberActions"], {
            "ok": self.onOk,
            "cancel": self.handleExit,
            "red": self.rotate,
            "green": self.close,
            "1": self.rotate
        }, -1)

        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.gotPicture)
        
        self.current_path = "/media"
        if not os.path.exists(self.current_path):
            self.current_path = "/"

        self.loadFiles(self.current_path)
        self["filelist"].onSelectionChanged.append(self.showPreview)

    def loadFiles(self, path):
        self.current_path = os.path.abspath(path)
        display_list = []
        try:
            if self.current_path != "/":
                display_list.append(".. (Parent Directory)")

            items = sorted(os.listdir(self.current_path))
            for f in items:
                if os.path.isdir(os.path.join(self.current_path, f)) and not f.startswith('.'):
                    display_list.append(f + "/")
            for f in items:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    display_list.append(f)
        except: pass
        
        self["filelist"].setList(display_list)
        self["status"].setText(self.current_path)

    def onOk(self):
        sel = self["filelist"].getCurrent()
        if not sel: return
        if sel == ".. (Parent Directory)":
            parent = os.path.dirname(self.current_path)
            self.loadFiles(parent)
        elif sel.endswith("/"):
            self.loadFiles(os.path.join(self.current_path, sel.rstrip("/")))
        else:
            self.session.open(FullScreenImage, os.path.join(self.current_path, sel))

    def handleExit(self):
        if self.current_path == "/": self.close()
        else:
            parent = os.path.dirname(self.current_path)
            self.loadFiles(parent)

    def showPreview(self):
        sel = self["filelist"].getCurrent()
        if not sel or sel.endswith("/") or sel.startswith(".."):
            self["preview"].hide()
            return
        self.picload.setPara((780, 600, 1, 1, False, 1, "#000000"))
        self.picload.startDecode(os.path.join(self.current_path, sel))

    def gotPicture(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr:
            self["preview"].instance.setPixmap(ptr)
            self["preview"].show()

    def rotate(self):
        sel = self["filelist"].getCurrent()
        if not sel or sel.endswith("/") or sel.startswith(".."): return
        try:
            full_path = os.path.join(self.current_path, sel)
            img = Image.open(full_path)
            img = img.rotate(270, expand=True)
            img.save(full_path)
            self.showPreview()
        except: pass

# -------------------------------------------------------
# VISOR FULLSCREEN (ZOOM Y ROTACIÓN)
# -------------------------------------------------------
class FullScreenImage(Screen):
    skin = """
    <screen name="FullScreenImage" position="0,0" size="%d,%d" flags="wfNoBorder" backgroundColor="#000000">
        <widget name="image" position="0,0" size="%d,%d" zPosition="1" />
        
        <!-- Firma también en Fullscreen en ROJO -->
        <widget name="by_author_fs" position="%d,20" size="300,30" font="Regular;18" halign="right" foregroundColor="#ff0000" transparent="1" zPosition="3" />

        <eLabel position="20,20" size="500,45" backgroundColor="#80000000" zPosition="2" />
        <ePixmap pixmap="buttons/red.png" position="30,30" size="35,25" alphatest="on" zPosition="3" />
        <widget name="key_red" position="70,30" size="100,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" zPosition="3" />
        <ePixmap pixmap="buttons/yellow.png" position="180,30" size="35,25" alphatest="on" zPosition="3" />
        <widget name="key_yellow" position="220,30" size="100,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" zPosition="3" />
        <ePixmap pixmap="buttons/blue.png" position="330,30" size="35,25" alphatest="on" zPosition="3" />
        <widget name="key_blue" position="370,30" size="100,30" font="Regular;20" foregroundColor="#ffffff" transparent="1" zPosition="3" />
    </screen>
    """ % (dw, dh, dw, dh, dw - 320)

    def __init__(self, session, image_path):
        Screen.__init__(self, session)
        self["image"] = Pixmap()
        self["by_author_fs"] = Label("by Zoubair91")
        self["key_red"] = Label("Rotate")
        self["key_yellow"] = Label("Zoom +")
        self["key_blue"] = Label("Zoom -")
        self.image_path = image_path
        self.zoom = 1.0
        self.off_x = 0
        self.off_y = 0

        self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "NumberActions"], {
            "cancel": self.close,
            "ok": self.handleOk,
            "left": self.left,
            "right": self.right,
            "up": self.up,
            "down": self.down,
            "yellow": self.zoomIn,
            "blue": self.zoomOut,
            "red": self.rotate,
            "1": self.rotate
        }, -1)

        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.gotPicture)
        self.images = []
        self.index = 0
        self.loadImageList()
        self.onLayoutFinish.append(self.refresh)

    def loadImageList(self):
        directory = os.path.dirname(self.image_path)
        try:
            self.images = [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            self.index = self.images.index(self.image_path)
        except: self.images = [self.image_path]

    def gotPicture(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr and self["image"].instance:
            self["image"].instance.setPixmap(ptr)

    def handleOk(self):
        if self.zoom > 1.0: self.reset()
        else: self.close()

    def left(self):
        if self.zoom > 1.0: self.off_x += 80; self.refresh()
        else: self.prev()

    def right(self):
        if self.zoom > 1.0: self.off_x -= 80; self.refresh()
        else: self.next()

    def up(self):
        if self.zoom > 1.0: self.off_y += 80; self.refresh()

    def down(self):
        if self.zoom > 1.0: self.off_y -= 80; self.refresh()

    def zoomIn(self):
        if self.zoom < 5.0: self.zoom += 0.5; self.refresh()

    def zoomOut(self):
        if self.zoom > 1.0: self.zoom -= 0.5; self.refresh()
        else: self.reset()

    def rotate(self):
        try:
            img = Image.open(self.image_path)
            img = img.rotate(270, expand=True)
            img.save(self.image_path)
            self.refresh()
        except: pass

    def next(self):
        self.index = (self.index + 1) % len(self.images)
        self.image_path = self.images[self.index]
        self.reset()

    def prev(self):
        self.index = (self.index - 1) % len(self.images)
        self.image_path = self.images[self.index]
        self.reset()

    def reset(self):
        self.zoom = 1.0
        self.off_x = 0
        self.off_y = 0
        self.refresh()

    def refresh(self):
        if not self["image"].instance: return
        new_w, new_h = int(dw * self.zoom), int(dh * self.zoom)
        pos_x, pos_y = (dw - new_w) // 2 + self.off_x, (dh - new_h) // 2 + self.off_y
        self["image"].instance.move(ePoint(pos_x, pos_y))
        self["image"].instance.resize(eSize(new_w, new_h))
        self.picload.setPara((new_w, new_h, 1, 1, False, 1, "#000000"))
        self.picload.startDecode(self.image_path)

# -------------------------------------------------------
# REGISTRO DEL PLUGIN (CON ICONO)
# -------------------------------------------------------
def main(session, **kwargs):
    session.open(PhotoBrowserScreen)

def Plugins(**kwargs):
    path = os.path.dirname(__file__)
    icon_file = os.path.join(path, "plugin.png")
    if not os.path.exists(icon_file):
        icon_file = None

    return PluginDescriptor(
        name="PhotoBrowser", 
        description="Browse photos (HDD/USB/Root) with Zoom & Rotate", 
        where=PluginDescriptor.WHERE_PLUGINMENU, 
        icon=icon_file,
        fnc=main
    )
