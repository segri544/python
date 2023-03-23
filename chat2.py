# from PyQt5.QtCore import QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

# class MapWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.map = QWebEngineView()
#         self.map.load(QUrl('https://www.google.com/maps/'))
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.map)

# app = QApplication([])
# widget = MapWidget()
# widget.show()
# app.exec_()

import folium

# Define the locations of your points
locations = [[39.94523994189189, 32.84516220237323],
             [40.01388005862508, 32.82191774559056],
             [40.02912623372994, 32.922680277455874],
             [39.96764748940887, 32.79920132105272]]

# Create a folium map and add the polyline layer
m = folium.Map(location=[39.99671092473233, 32.82893015884888], zoom_start=12)

# Create a PolyLine object
polyline = folium.PolyLine(locations=locations, color='red')

# Add the PolyLine object to the map
polyline.add_to(m)

# Display the map
m.save('map.html')