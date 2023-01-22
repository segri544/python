class DroneDataWindow(QMainWindow):
    def __init__(self):
        # ...
        # Create graphics view and scene
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.layout.addWidget(self.graphics_view)
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        self.graphics_view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.graphics_view.setRenderHint(QPainter.HighQualityAntialiasing)
        self.graphics_view.setRenderHint(QPainter.TextAntialiasing)
        self.graphics_view.setRenderHint(QPainter.NonCosmeticDefaultPen)
        self.graphics_view.setRenderHint(QPainter.Qt4CompatiblePainting)
        
        # Create line
        self.line = QGraphicsLineItem()
        self.graphics_scene.addItem(self.line)
        self.line.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        self.line.setLine(0, 0, 100, 100)
        self.line.setLine(long1, lat1, long2, lat2)
        def mousePressEvent(self, event):
            self.start_point = self.graphics_view.mapToScene(event.pos())
            
        def mouseReleaseEvent(self, event):
            self.end_point = self.graphics_view.mapToScene(event.pos())
            self.line.setLine(self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y())