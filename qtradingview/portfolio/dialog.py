from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QLocale

from qtradingview.ui.Ui_dialog_trade import Ui_DialogTrade
from qtradingview.models.markets import Markets
from .models import Trades


# ─── DIALOG TRADE ───────────────────────────────────────────────────────────────

class DialogTrade(QDialog, Ui_DialogTrade):
    
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        QDialog.__init__(self, parent=parent, flags=flags)
        self.setupUi(self)
        #
        self.spin_price.setLocale(QLocale('C'))
        self.spin_amount.setLocale(QLocale('C'))

    def loadNewTradeData(self, exchange, market):
        self.ed_exchange.setText(exchange.title())
        self.ed_market.setText(market.upper())
        self.m = Markets.get_symbol_by_exchange(self.ed_market.text(), self.ed_exchange.text())
        self.spin_price.setValue(self.m.last_price)
        self.spin_price.setSingleStep(self.m.last_price * 0.01)

    def loadEditTradeData(self, trade_id):
        self.t = Trades.get_by_id(trade_id)
        self.ed_exchange.setText(self.t.market.exchange.title())
        self.ed_market.setText(self.t.market.symbol.upper())
        index = self.combo_type.findText(self.t.position.title())
        self.combo_type.setCurrentIndex(index)
        self.spin_price.setValue(self.t.open_price)
        self.spin_price.setSingleStep(self.t.open_price * 0.01)
        self.spin_amount.setValue(self.t.amount)

    def createTrade(self):
        t = Trades(
            market=self.m, position=self.combo_type.currentText().lower(),
            open_price=self.spin_price.value(), amount=self.spin_amount.value()
        )
        t.save()

    def updateTrade(self):
        self.t.position = self.combo_type.currentText().lower()
        self.t.open_price = self.spin_price.value()
        self.t.amount = self.spin_amount.value()
        self.t.save()
        
# ────────────────────────────────────────────────────────────────────────────────
