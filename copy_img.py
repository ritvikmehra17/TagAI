from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication
import os, sys

def copy():
    app = QApplication(sys.argv)
    file = r"/path/to/image/grid-of-tiles.png"

    # image I'm using has these many rows and columns of tiles
    r = 57
    c = 50

    mosaic = QImage(file) # QImage instead of QPixmap

    # the tiles are known to divide evenly
    width = mosaic.width() / c
    height = mosaic.height() / r

    # much less memory!
    minipixmaps = [QPixmap.fromImage(mosaic.copy(row*height, col*width, width, height)) for row in range(r) for col in range(c)]