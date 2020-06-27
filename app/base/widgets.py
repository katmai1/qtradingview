import logging

from PyQt5.QtWidgets import QSplashScreen, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from PyQt5.QtWebEngineWidgets import QWebEnginePage


# ─── CUSTOM WEBENGINEPAGE ───────────────────────────────────────────────────────

class CustomWebEnginePage(QWebEnginePage):

    adblocker_2020 = """
        (
            function() {
                'use strict';
                const checkAd = setInterval(() => {
                    const adBox = document.getElementById('tv-toasts');
                    if (adBox) {    adBox.remove(); }
                    const adWrapper = $("div[class^='toast-positioning-wrapper-']")[0];
                    if (adWrapper)  {   adWrapper.style.display = "none";   }
                }, 1500);
            }
        )();"""

    def __init__(self, parent):
        super().__init__(parent)
        self.mw = self.parent().parent().parent()
        #
        self.timer_titulo = QTimer(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.loadStarted.connect(self._on_load_started)
        self.timer_titulo.timeout.connect(self.update_titulo)

    # al iniciar una carga detiene el timer que elimina la publicidad
    def _on_load_started(self):
        self.clear_titulo()
        self.timer_titulo.stop()

    # al finalizar la carga activa el adblocker y updater titulo
    def _on_load_finished(self):
        self.html = self.toHtml(self._get_html)
        self.timer_titulo.start(3000)
        self.adblocker_tradingview()

    def clear_titulo(self):
        self.mw.setWindowTitle("QTradingView")

    # actualiza el titulo de la ventana con el market y precio actual
    def update_titulo(self):
        try:
            v = self.title().split(" ")
            titulo = f"{v[0]} {v[1]} {v[2]} | QTradingView"
        except Exception as e:
            logging.debug(f"can't read title, market not load? {e}")
            titulo = "QTradingView"
        finally:
            self.mw.setWindowTitle(titulo)

    # funcion necesaria para ver el codigo html (toHtml)
    def _get_html(self, html_str):
        self.html = html_str
        # logging.debug(html_str)

    # javascripts
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        logging.debug(msg)

    def adblocker_tradingview(self):
        self.runJavaScript(self.adblocker_2020)

# ────────────────────────────────────────────────────────────────────────────────


# ─── SPLASH SCREEN ──────────────────────────────────────────────────────────────

class CustomSplashScreen(QSplashScreen):

    imagen = ":/base/splash"

    def __init__(self, parent=None):
        screen_size = QDesktopWidget().screenGeometry(-1)
        pixmap = QPixmap(self.imagen).scaledToWidth(screen_size.width() / 3)
        super().__init__(parent, pixmap, Qt.SplashScreen)
        self.setMask(pixmap.mask())
        self.set_texto("Loading")
        self.show()

    def set_texto(self, texto, size=3):
        self.showMessage(f"<h{size}>{self.tr(texto)}</h{size}>", Qt.AlignCenter | Qt.AlignBottom)

# ────────────────────────────────────────────────────────────────────────────────
