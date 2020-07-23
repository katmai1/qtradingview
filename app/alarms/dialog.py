from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QLocale

from app.ui.dialog_alarm_Ui import Ui_dialogAlarm
from app.models.markets import Markets
from .models import Alarms


# ─── DIALOG ALARMS ──────────────────────────────────────────────────────────────

class DialogAlarm(QDialog, Ui_dialogAlarm):
    
    def __init__(self, exchange, market, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        #
        # load market info
        self.ed_exchange.setText(exchange.title())
        self.ed_market.setText(market.upper())
        self.m = Markets.get_symbol_by_exchange(self.ed_market.text(), self.ed_exchange.text())
        self.ed_lastPrice.setText(f"{self.m.last_price:.8}")
        # load conditions
        for c in Alarms.CONDITIONS_CHOICES:
            self.cb_condition.addItem(c[1], c[0])
        # config spin
        self.spin_price.setLocale(QLocale('C'))
        self.spin_price.setMaximum(self.m.last_price * 100)
        self.spin_price.setSingleStep(self.m.last_price * 0.005)

    def loadNewAlarm(self):
        self.spin_price.setValue(self.m.last_price)
    
    def createAlarm(self):
        al = Alarms(
            market=self.m, condition=self.cb_condition.currentData(), price=self.spin_price.value()
        )
        al.save()

# ────────────────────────────────────────────────────────────────────────────────
