from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QLocale

from qtradingview.ui.dialog_alarm_Ui import Ui_dialogAlarm
from qtradingview.models.markets import Markets
from .models import Alarms


# ─── DIALOG ALARMS ──────────────────────────────────────────────────────────────

class DialogAlarm(QDialog, Ui_dialogAlarm):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        #
        for c in Alarms.CONDITIONS_CHOICES:
            self.cb_condition.addItem(c[1], c[0])
        self.spin_price.setLocale(QLocale('C'))

    def loadNewAlarm(self, exchange, market):
        """ Load data to create new alarm """
        self.ed_exchange.setText(exchange.title())
        self.ed_market.setText(market.upper())
        self.m = Markets.get_symbol_by_exchange(self.ed_market.text(), self.ed_exchange.text())
        self.ed_lastPrice.setText(f"{self.m.last_price:.8}")
        self.spin_price.setMaximum(self.m.last_price * 100)
        self.spin_price.setSingleStep(self.m.last_price * 0.005)
        self.spin_price.setValue(self.m.last_price)

    def loadAlarm(self, alarm_id):
        """ Load data from alarm """
        alarm = Alarms.get_by_id(alarm_id)
        self.ed_exchange.setText(alarm.market.exchange)
        self.ed_market.setText(alarm.market.symbol)
        self.ed_lastPrice.setText(f"{alarm.market.last_price:.8}")
        self.cb_condition.setCurrentIndex(alarm.condition)
        self.ck_autodelete.setChecked(alarm.autodelete)
        self.spin_price.setMaximum(alarm.market.last_price * 100)
        self.spin_price.setSingleStep(alarm.market.last_price * 0.005)
        self.spin_price.setValue(alarm.price)

    def createAlarm(self):
        """ Save data to new alarm """
        al = Alarms(
            market=self.m, condition=self.cb_condition.currentData(),
            price=self.spin_price.value(), autodelete=self.ck_autodelete.isChecked()
        )
        al.save()

    def updateAlarm(self, alarm_id):
        """ Update data of alarm """
        alarm = Alarms.get_by_id(alarm_id)
        alarm.condition = self.cb_condition.currentData()
        alarm.price = self.spin_price.value()
        alarm.autodelete = self.ck_autodelete.isChecked()
        alarm.save()

# ────────────────────────────────────────────────────────────────────────────────
