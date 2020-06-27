from PyQt5.QtWidgets import QDialog, QMessageBox
from copy import copy

from app.models.markets import Markets
from app.ui.dialog_config_Ui import Ui_DialogConfig


# ─── CONFIG DIALOG ──────────────────────────────────────────────────────────────

class DialogConfig(QDialog, Ui_DialogConfig):

    def __init__(self, parent=None, *args, **kwargs):
        QDialog.__init__(self, parent=parent, *args, **kwargs)
        self.setupUi(self)
        self.mw = parent
        #
        self.list_exchanges.sortItems()
        self.config = self.mw.ctx.config
        self._add_languages()
        self.combo_initial_exchange.currentTextChanged.connect(self.onSelectInitialExchange)
        self.combo_languages.currentTextChanged.connect(self.onChangeLanguage)

    def _add_languages(self):
        self.combo_languages.blockSignals(True)
        self.combo_languages.addItem(self.tr("Spanish"), "es_ES")
        self.combo_languages.addItem(self.tr("English"), "en_EN")

    @property
    def exchanges_is_changed(self):
        """ Return true if exchanges list is modified """
        return self.old_config["exchanges"] != self.config["exchanges"]

    # ─── EVENTOS ────────────────────────────────────────────────────────────────────

    def onChangeLanguage(self, language):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle(self.tr("Language changed"))
        mbox.setText(self.tr("The language change will be applied when restarting the application"))
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.show()

    def onSelectInitialExchange(self):
        """ Load initial markets of selected initial exchange """
        self.combo_initial_market.clear()
        for it in Markets.get_all_by_exchange(self.combo_initial_exchange.currentText().lower()):
            self.combo_initial_market.addItem(it.symbol)
        index = self.combo_initial_market.findText(self.config['initial_market'])
        self.combo_initial_market.setCurrentIndex(index)

    # ─── load methods ───────────────────────────────────────────────────────

    def load_config(self, config):
        """ Load config in form widgets """
        self._select_exchanges(config['exchanges'])
        self._select_language(config['language'])
        self._select_initial_exchange()
        self.old_config = copy(config)
        self.combo_languages.blockSignals(False)

    def _select_initial_exchange(self):
        """ Select initial exchange configured in config file """
        index = self.combo_initial_exchange.findText(self.config['initial_exchange'])
        self.combo_initial_exchange.setCurrentIndex(index)

    def _select_exchanges(self, exchanges):
        """ Select exchanges actived in config file """
        for index in range(self.list_exchanges.count()):
            item = self.list_exchanges.item(index)
            if item.text() in self.config['exchanges']:
                item.setSelected(True)
            # añade la lista al combo de paso
            self.combo_initial_exchange.addItem(item.text())

    def _select_language(self, language):
        """ Select language defined in config file """
        index = self.combo_languages.findData(language)
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
        self.config['language'] = self.combo_languages.currentData()
        self.config['exchanges'] = self._get_list_exchanges()
        self.config['initial_exchange'] = self.combo_initial_exchange.currentText()
        self.config['initial_market'] = self.combo_initial_market.currentText()
        self.mw.ctx.save_config()
        return super().accept()
# ────────────────────────────────────────────────────────────────────────────────
