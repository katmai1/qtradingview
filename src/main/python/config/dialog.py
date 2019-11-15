from PyQt5 import QtWidgets
from ui.dialog_config_Ui import Ui_DialogConfig


class DialogConfig(QtWidgets.QDialog, Ui_DialogConfig):

    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)

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

# ────────────────────────────────────────────────────────────────────────────────
