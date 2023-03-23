from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

app = QApplication([])
window = QWidget()

map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
marker = folium.Marker(location=[51.5074, -0.1278], popup='London')
marker.add_to(map)
html = map.get_root().render()

view = QWebEngineView()
view.setHtml(html)
view.setGeometry(100, 100, 800, 600)

window.show()
QApplication.processEvents()
app.exec_()
