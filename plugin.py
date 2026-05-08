from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap
from enigma import ePicLoad, ePoint, eSize, getDesktop
from Plugins.Plugin import PluginDescriptor
import os

# Pillow (con fallback seguro)
try:
    from PIL import Image
except:
    Image = None

# Resolución pantalla
dw = getDesktop(0).size().width()
dh = getDesktop(0).size().height()

# -------------------------------------------------------
# EXPLORADOR DE FOTOS
# -------------------------------------------------------
class PhotobrowserScreen(Screen):

    skin = """
    <screen name="Photobrowser" position="center,center" size="1200,720" title="Photobrowser" backgroundColor="#101010" flags="wfNoBorder">

        <eLabel position="0,0" size="380,720" backgroundColor="#1a1a1a" zPosition="-1" />

        <widget name="by_author" position="800,20" size="380,30" font="Regular;22" halign="right" foregroundColor="#ff0000" transparent="1" />

        <widget name="filelist" position="20,80" size="340,540" itemHeight="45" scrollbarMode="showOnDemand" transparent="1" />

        <widget name="status" position="20,20" size="340,50" font="Regular;18" foregroundColor="#00ff00" transparent="1" />

        <eLabel position="380,0" size="820,720" backgroundColor="#000000" zPosition="-1" />

        <widget name="preview" position="400,60" size="780,600" alphatest="blend" />

        <widget name="key_info" position="20,670" size="1100,30" font="Regular;18" foregroundColor="#888888" transparent="1" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)

        self["filelist"] = MenuList([])
        self["preview"] = Pixmap()
        self["status"] = Label("")
        self["by_author"] = Label("by theking-cs")
        self["key_info"] = Label("OK Open | EXIT Back | RED Rotate")

        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.openFile,
            "cancel": self.exit,
            "red": self.rotate
        }, -1)

        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.showPreview)

        self.current_path = "/media"
        if not os.path.exists(self.current_path):
            self.current_path = "/"

        self.loadFiles(self.current_path)
        self["filelist"].onSelectionChanged.append(self.updatePreview)

    # ---------------------------------------------------

    def loadFiles(self, path):
        self.current_path = os.path.abspath(path)
        list_files = []

        try:
            if self.current_path != "/":
                list_files.append("..")

            items = sorted(os.listdir(self.current_path))

            for i in items:
                full = os.path.join(self.current_path, i)

                if os.path.isdir(full):
                    list_files.append(i + "/")

            for i in items:
                if i.lower().endswith((".jpg", ".jpeg", ".png")):
                    list_files.append(i)

        except Exception as e:
            print("[Photobrowser]", e)

        self["filelist"].setList(list_files)
        self["status"].setText(self.current_path)

    # ---------------------------------------------------

    def openFile(self):
        sel = self["filelist"].getCurrent()
        if not sel:
            return

        if sel == "..":
            self.loadFiles(os.path.dirname(self.current_path))

        elif sel.endswith("/"):
            self.loadFiles(os.path.join(self.current_path, sel[:-1]))

        else:
            self.session.open(FullScreenImage, os.path.join(self.current_path, sel))

    # ---------------------------------------------------

    def exit(self):
        self.close()

    # ---------------------------------------------------

    def updatePreview(self):
        sel = self["filelist"].getCurrent()

        if not sel or sel.endswith("/"):
            return

        path = os.path.join(self.current_path, sel)

        self.picload.setPara((780, 600, 1, 1, False, 1, "#000000"))
        self.picload.startDecode(path)

    def showPreview(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr:
            self["preview"].instance.setPixmap(ptr)
            self["preview"].show()

    # ---------------------------------------------------

    def rotate(self):
        if Image is None:
            return

        sel = self["filelist"].getCurrent()
        if not sel or sel.endswith("/"):
            return

        try:
            path = os.path.join(self.current_path, sel)
            img = Image.open(path)
            img = img.rotate(270, expand=True)
            img.save(path)
            self.updatePreview()
        except Exception as e:
            print("[Photobrowser rotate]", e)

# -------------------------------------------------------
# FULLSCREEN VIEWER
# -------------------------------------------------------
class FullScreenImage(Screen):

    skin = """
    <screen name="FullScreen" position="0,0" size="%d,%d" flags="wfNoBorder" backgroundColor="#000000">
        <widget name="image" position="0,0" size="%d,%d" />
    </screen>
    """ % (dw, dh, dw, dh)

    def __init__(self, session, path):
        Screen.__init__(self, session)

        self.path = path
        self["image"] = Pixmap()

        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.paint)

        self.onLayoutFinish.append(self.load)

    def load(self):
        self.picload.setPara((dw, dh, 1, 1, False, 1, "#000000"))
        self.picload.startDecode(self.path)

    def paint(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr:
            self["image"].instance.setPixmap(ptr)

# -------------------------------------------------------
# PLUGIN ENTRY
# -------------------------------------------------------
def main(session, **kwargs):
    session.open(PhotobrowserScreen)

def Plugins(**kwargs):
    return PluginDescriptor(
        name="Photobrowser",
        description="Photo viewer for Enigma2",
        where=PluginDescriptor.WHERE_PLUGINMENU,
        fnc=main
    )
