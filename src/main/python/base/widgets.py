import logging

from PyQt5.QtWidgets import QSplashScreen, QDesktopWidget
from PyQt5.QtCore import Qt, QCoreApplication
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

    adblocker_js_reduced = """
        (
            function() {
                'use strict';
                const checkAd = setInterval(() => {
                    const adBox = document.getElementById('tv-toasts');
                    if (adBox) {    adBox.remove(); }
                }, 5000);
            }
        )();"""

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        logging.debug(msg)

    def adblocker_tradingview(self):
        self.runJavaScript(self.adblocker_js_reduced)

# ────────────────────────────────────────────────────────────────────────────────


# ─── SPLASH SCREEN ──────────────────────────────────────────────────────────────

class CustomSplashScreen(QSplashScreen):

    imagen = ":/base/splash.png"

    def __init__(self, parent=None):
        screen_size = QDesktopWidget().screenGeometry(-1)
        pixmap = QPixmap(self.imagen).scaledToWidth(screen_size.width() / 3)
        super().__init__(parent, pixmap, Qt.SplashScreen)
        self.setMask(pixmap.mask())
        mensaje = QCoreApplication.translate("splash", "Cargando...")
        self.set_texto(mensaje)

    def set_texto(self, texto, size=3):
        self.showMessage(f"<h{size}>{texto}</h{size}>", Qt.AlignCenter | Qt.AlignBottom)

# ────────────────────────────────────────────────────────────────────────────────
