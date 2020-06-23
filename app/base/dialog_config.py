from PyQt5 import QtWidgets, uic
import logging
import toml
import os

from app.models.markets import Markets
from app.utils import resource_path
from app.ui.dialog_config_Ui import Ui_DialogConfig

# ─── CONFIG DIALOG ──────────────────────────────────────────────────────────────

# ui_filename = os.path.join("ui", "dialog_config.ui")
# Ui_DialogConfig, QtBaseClass = uic.loadUiType(resource_path(ui_filename))


class DialogConfig(QtWidgets.QDialog, Ui_DialogConfig):

    exchanges = ["Bittrex", 'Bitfinex', 'Binance', 'Poloniex', 'Kraken']

    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, parent=parent, *args, **kwargs)
        # Ui_DialogConfig.__init__(self)
        self.setupUi(self)
        self.mw = parent
        #
        self.config = self.parent().ctx.config
        self.combo_initial_exchange.currentTextChanged.connect(self.onSelectInitialExchange)

    def load_config(self, config):
        self._load_exchanges(config['exchanges'])
        self._select_language(config['language'])
        self._select_initial_exchange()

    def onSelectInitialExchange(self):
        self.combo_initial_market.clear()
        for it in Markets.get_all_by_exchange(self.combo_initial_exchange.currentText().lower()):
            self.combo_initial_market.addItem(it.symbol)
        index = self.combo_initial_market.findText(self.config['initial_market'])
        self.combo_initial_market.setCurrentIndex(index)

    # carga lista de exchanges iniciales y selecciona el configurado
    def _select_initial_exchange(self):
        self.combo_initial_exchange.addItems(self.exchanges)
        index = self.combo_initial_exchange.findText(self.config['initial_exchange'])
        self.combo_initial_exchange.setCurrentIndex(index)

    # carga lista de exchanges y selecciona los configurados
    def _load_exchanges(self, exchanges):
        self.list_exchanges.addItems(self.exchanges)
        for index in range(self.list_exchanges.count()):
            item = self.list_exchanges.item(index)
            if item.text() in self.config['exchanges']:
                item.setSelected(True)

    # selecciona el idioma configurado
    def _select_language(self, language):
        index = self.combo_languages.findText(language)
        self.combo_languages.setCurrentIndex(index)

    # devuelve lista de los exchanges seleccionados
    def _get_list_exchanges(self):
        lista = []
        for index in range(self.list_exchanges.count()):
            item = self.list_exchanges.item(index)
            if item.isSelected():
                lista.append(item.text())
        return lista

    # actualiza self.config y guarda cambios al fichero
    def accept(self):
        self.config['language'] = self.combo_languages.currentText()
        self.config['exchanges'] = self._get_list_exchanges()
        self.config['initial_exchange'] = self.combo_initial_exchange.currentText()
        self.config['initial_market'] = self.combo_initial_market.currentText()
        self.parent().ctx.save_config()
        self.mw.dock_markets._load_exchanges()
        return super().accept()
# ────────────────────────────────────────────────────────────────────────────────
