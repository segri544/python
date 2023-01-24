import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication


def callback_function(html):
    print(html)


def on_load_finished():
    web.page().runJavaScript(
        "document.getElementsByTagName('html')[0].innerHTML", callback_function
    )
    # or document.getElementsByTagName('html')[0].outerHTML


app = QApplication(sys.argv)
web = QWebEngineView()
web.load(QUrl("https://stackoverflow.com"))
web.show()
web.resize(640, 480)
web.loadFinished.connect(on_load_finished)

sys.exit(app.exec_())