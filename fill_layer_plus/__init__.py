from krita import Krita

from .fill_layer_plus import FillLayerPlusExtension

Krita.instance().addExtension(FillLayerPlusExtension(Krita.instance()))
