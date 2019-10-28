import logging

from PyQt5.QtWidgets import QSplashScreen, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtWebEngineWidgets import QWebEnginePage


# ─── CUSTOM WEBENGINEPAGE ───────────────────────────────────────────────────────

class CustomWebEnginePage(QWebEnginePage):

    adblocker_js = """(function() {
                'use strict';
                const checkAd = setInterval(() => {
                    const adBox = document.getElementById('tv-toasts');
                    if (adBox) {
                    adBox.remove();
                    console.log('ad removed.');
                    } else {
                    console.log('no ad present.');
                    }
                }, 5000);
                })();"""

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        logging.debug(msg)

    def adblocker_tradingview(self):
        self.runJavaScript(self.adblocker_js)

# ────────────────────────────────────────────────────────────────────────────────


# ─── SPLASH SCREEN ──────────────────────────────────────────────────────────────

class CustomSplashScreen(QSplashScreen):

    imagen = ":/base/splash.png"

    def __init__(self, parent=None):
        screen_size = QDesktopWidget().screenGeometry(-1)
        pixmap = QPixmap(self.imagen).scaledToWidth(screen_size.width()/3)
        super().__init__(parent, pixmap, Qt.SplashScreen)
    
    def set_texto(self, texto, size=3):
        self.showMessage(f"<h{size}>{texto.title()}</h{size}>", Qt.AlignCenter | Qt.AlignBottom)

# ────────────────────────────────────────────────────────────────────────────────

