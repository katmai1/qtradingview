from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication as qapp

from ui.dialog_alarm_Ui import Ui_dialogAlarm

from models.markets import Markets, Alarms


class DialogAlarm(QtWidgets.QDialog, Ui_dialogAlarm):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def new_alarm(self, exchange, market):
        self.setWindowTitle(qapp.tr("Nueva alarma"))
        itemdb = Markets.get_symbol_by_exchange(market, exchange)
        self.alarm = Alarms(market=itemdb, description=market)
        self._load_info()
        self.spin_price.setValue(float(self.ed_currentPrice.text()))

    def edit_alarm(self, id_alarm):
        self.setWindowTitle(qapp.tr("Editar alarma") + f" #{id_alarm}")
        self.alarm = Alarms.get_by_id(id_alarm)
        self._load_info()
        self.spin_price.setValue(self.alarm.price)
        self.check_autodelete.setChecked(self.alarm.autodelete)
        self.combo_condition.setCurrentIndex(self.alarm.condition)

    def accept(self):
        self.alarm.condition = self.combo_condition.currentIndex()
        self.alarm.price = self.spin_price.value()
        self.alarm.autodelete = self.check_autodelete.isChecked()
        self.alarm.save()
        return super().accept()

    def _load_info(self):
        self.ed_exchange.setText(self.alarm.market.exchange.title())
        self.ed_market.setText(self.alarm.market.symbol)
        self.spin_price.setMaximum(self.alarm.market.limit_max_price)
        self.spin_price.setMinimum(self.alarm.market.limit_min_price)
        last = self.alarm.market.last_price
        self.spin_price.setSingleStep(last * 0.005)
        self.spin_price.setSuffix(self.alarm.market.symbol.split("/")[1])
        self.ed_currentPrice.setText("%.8f" % last)
