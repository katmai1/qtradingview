from PyQt5.QtWidgets import QDialog, QMessageBox

from qtradingview.models.markets import Markets
from qtradingview.ui.Ui_dialog_config import Ui_DialogConfig


# ─── CONFIG DIALOG ──────────────────────────────────────────────────────────────

class DialogConfig(QDialog, Ui_DialogConfig):

    def __init__(self, parent=None, *args, **kwargs):
        QDialog.__init__(self, parent=parent, *args, **kwargs)
        self.setupUi(self)
        self.mw = parent
        #
        self.list_exchanges.sortItems()
        self.cfg = self.mw.ctx.settings
        #
        self.loadConfig()
        self.combo_initial_exchange.currentTextChanged.connect(self.onSelectInitialExchange)
        self.combo_languages.currentTextChanged.connect(self.onChangeLanguage)
        self.onSelectInitialExchange()

    def loadConfig(self):
        # add language
        self.combo_languages.addItem(self.tr("Spanish"), "es_ES")
        self.combo_languages.addItem(self.tr("English"), "en_EN")
        self._select_language(self.cfg.value("settings/language"))
        # exchanges list and initial exchange
        self._select_exchanges(self.cfg.value("settings/exchanges"))
        self._select_initial_exchange()
        # copy exchanges list actived to compare on exit
        self.old_exchanges = self.cfg.value("settings/exchanges")
     
    @property
    def exchanges_is_changed(self):
        """ Return true if exchanges list is modified """
        return self.old_exchanges != self.cfg.value("settings/exchanges")

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
        index = self.combo_initial_market.findText(self.cfg.value("settings/initial_market"))
        self.combo_initial_market.setCurrentIndex(index)

    # ─── load methods ───────────────────────────────────────────────────────

    def _select_initial_exchange(self):
        """ Select initial exchange configured in config file """
        index = self.combo_initial_exchange.findText(self.cfg.value("settings/initial_exchange"))
        self.combo_initial_exchange.setCurrentIndex(index)

    def _select_exchanges(self, exchanges):
        """ Select exchanges actived in config file """
        for index in range(self.list_exchanges.count()):
            item = self.list_exchanges.item(index)
            if item.text() in exchanges:
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
        self.cfg.setValue("settings/language", self.combo_languages.currentData())
        self.cfg.setValue("settings/exchanges", self._get_list_exchanges())
        self.cfg.setValue("settings/initial_exchange", self.combo_initial_exchange.currentText())
        self.cfg.setValue("settings/initial_market", self.combo_initial_market.currentText())
        return super().accept()
# ────────────────────────────────────────────────────────────────────────────────
