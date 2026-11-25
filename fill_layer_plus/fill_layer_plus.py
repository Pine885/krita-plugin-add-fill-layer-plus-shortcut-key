from krita import Extension, InfoObject, Krita, Selection
from PyQt5.QtCore import QStandardPaths
import filecmp
import os
import shutil

from .core import insertion_point, next_layer_name

ACTION_ID = "fill_layer_plus_foreground"
ACTION_TEXT = "Fill Layer with Foreground Color"
ACTION_FILE = "fill_layer_plus_foreground.action"


class FillLayerPlusExtension(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.plugin_dir = os.path.dirname(__file__)

    def setup(self):
        self.install_action_file()

    def createActions(self, window):
        action = window.createAction(ACTION_ID, ACTION_TEXT, "tools/scripts")
        action.triggered.connect(self.create_foreground_fill_layer)

    def install_action_file(self):
        try:
            actions_dir = os.path.join(
                QStandardPaths.writableLocation(QStandardPaths.AppDataLocation),
                "actions")
            os.makedirs(actions_dir, exist_ok=True)

            src = os.path.join(self.plugin_dir, ACTION_FILE)
            dst = os.path.join(actions_dir, ACTION_FILE)

            if not os.path.exists(src):
                return
            if not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False):
                shutil.copyfile(src, dst)
        except Exception:
            pass

    def create_foreground_fill_layer(self):
        app = Krita.instance()
        doc = app.activeDocument()
        if not doc:
            return

        window = app.activeWindow()
        view = window.activeView() if window else None
        if not view:
            return

        foreground = view.foregroundColor()

        parent, above = insertion_point(doc.activeNode(), doc.rootNode())
        if parent is None:
            return

        info = InfoObject()
        info.setProperty("color", foreground.toXML())

        selection = doc.selection()
        if selection is None:
            bounds = doc.bounds()
            selection = Selection()
            selection.select(bounds.x(), bounds.y(),
                             bounds.width(), bounds.height(), 255)
        layer = doc.createFillLayer(
            next_layer_name(self._layer_names(doc.rootNode())),
            "color",
            info,
            selection)
        if layer is None:
            return

        if not parent.addChildNode(layer, above):
            return
        doc.setActiveNode(layer)

    def _layer_names(self, root):
        names = []
        stack = [root]
        while stack:
            node = stack.pop()
            names.append(node.name())
            for child in node.childNodes():
                if not child.type().endswith("mask"):
                    stack.append(child)
        return names
