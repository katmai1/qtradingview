from PyQt5 import QtWidgets
from copy import copy

from app.models.markets import Markets
from app.ui.dialog_config_Ui import Ui_DialogConfig


# ─── CONFIG DIALOG ──────────────────────────────────────────────────────────────

class DialogConfig(QtWidgets.QDialog, Ui_DialogConfig):

    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, parent=parent, *args, **kwargs)
        self.setupUi(self)
        self.mw = parent
        #
        self.list_exchanges.sortItems()
        self.config = self.mw.ctx.config
        self.combo_initial_exchange.currentTextChanged.connect(self.onSelectInitialExchange)

    # return true if changed list of exchanges
    @property
    def exchanges_is_changed(self):
        return self.old_config["exchanges"] != self.config["exchanges"]

    # ─── EVENTOS ────────────────────────────────────────────────────────────────────

    # carga la lista de markets nueva
    def onSelectInitialExchange(self):
        self.combo_initial_market.clear()
        for it in Markets.get_all_by_exchange(self.combo_initial_exchange.currentText().lower()):
            self.combo_initial_market.addItem(it.symbol)
        index = self.combo_initial_market.findText(self.config['initial_market'])
        self.combo_initial_market.setCurrentIndex(index)

    # ─── load methods ───────────────────────────────────────────────────────

    # carga la configuracion a los componentes
    def load_config(self, config):
        self._select_exchanges(config['exchanges'])
        self._select_language(config['language'])
        self._select_initial_exchange()
        self.old_config = copy(config)

    # carga combo de exchanges iniciales y selecciona el configurado
    def _select_initial_exchange(self):
        index = self.combo_initial_exchange.findText(self.config['initial_exchange'])
        self.combo_initial_exchange.setCurrentIndex(index)

    # selecciona los exchanges configurados
    def _select_exchanges(self, exchanges):
        for index in range(self.list_exchanges.count()):
            item = self.list_exchanges.item(index)
            if item.text() in self.config['exchanges']:
                item.setSelected(True)
            # añade la lista al combo de paso
            self.combo_initial_exchange.addItem(item.text())

    # selecciona el idioma configurado
    def _select_language(self, language):
        index = self.combo_languages.findText(language)
        self.combo_languages.setCurrentIndex(index)

    # ─── SAVING-EXIT METHODS ────────────────────────────────────────────────────────

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
        self.mw.ctx.save_config()
        return super().accept()
# ────────────────────────────────────────────────────────────────────────────────
