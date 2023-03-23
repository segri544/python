import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout, QWidget,QApplication
import sys

import time
class MapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # initialize folium map
        self.m = folium.Map(location=[39.94550315392756, 32.864044961167124], zoom_start=18)

        # add marker to map
        folium.Marker(
            location=[39.94550315392756, 32.864044961167124],
            popup='Boston',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(self.m)

        # create web view
        self.view = QWebEngineView()
        map_html = self.m._repr_html_()
        self.view.setHtml(map_html)
        
        # create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

    def clearMarkers(self):
        self.m.clear_layers()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWidget()
    window.showNormal()
    
    sys.exit(app.exec_())