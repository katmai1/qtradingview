from PyQt5 import QtWidgets
from ui.dialog_config_Ui import Ui_DialogConfig
import logging
import toml


class DialogConfig(QtWidgets.QDialog, Ui_DialogConfig):

    exchanges = ["bittrex", 'bitfinex', 'binance', 'poloniex']
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.config = self.parent().config

    def load_config(self, config):
        self._load_exchanges(config['exchanges'])
        self._select_language(config['language'])

    def _load_exchanges(self, exchanges):
        for exchange in exchanges:
            check = getattr(self, f"check_{exchange}", None)
            if check is not None:
                check.setChecked(True)

    def _select_language(self, language):
        index = self.combo_languages.findText(language)
        self.combo_languages.setCurrentIndex(index)

    def _get_list_exchanges(self):
        lista = []
        for exchange in self.exchanges:
            check = getattr(self, f"check_{exchange}", None)
            if check.isChecked():
                lista.append(exchange)
        return lista

    def accept(self):
        self.config['language'] = self.combo_languages.currentText()
        self.config['exchanges'] = self._get_list_exchanges()
        with open("/home/q/.qtradingview/config.toml", "w") as f:
            toml.dump(self.config, f)
        return super().accept()
# ────────────────────────────────────────────────────────────────────────────────
