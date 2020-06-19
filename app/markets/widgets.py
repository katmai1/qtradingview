from PyQt5.QtWidgets import QStyledItemDelegate, QListWidgetItem, QStyleOptionViewItem, QListWidget
from PyQt5.QtGui import QIcon

from models.markets import Markets


class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QStyleOptionViewItem.Right
        super(CustomItemDelegate, self).paint(painter, option, index)


class CustomItem(QListWidgetItem):

    exchange = None

    @property
    def symbol(self):
        return self.text()

    @property
    def is_favorite(self):
        return Markets.check_symbol_is_fav(self.symbol, self.exchange)
    
    @property
    def is_margin(self):
        return Markets.check_symbol_is_margin(self.symbol, self.exchange)

    def _get_icon(self):
        if self.is_favorite:
            return QIcon(":/base/star")
        return QIcon(":/base/voidstar")

    def _mostrar(self):
        self.setHidden(False)

    def _ocultar(self):
        self.setHidden(True)

    def configurar(self, symbol, exchange):
        self.setText(symbol)
        self.exchange = exchange.lower()
        self.setIcon(self._get_icon())

    def mostrar(self, lista_mode, filtro):
        if lista_mode == "all":
            self.mostrar_all(True, filtro)
        elif lista_mode == "fav":
            self.mostrar_fav(True, filtro)
        elif lista_mode == "margin":
            self.mostrar_margin(True, filtro)

    def mostrar_all(self, all_actived, filtro):
        if all_actived:
            if filtro.upper() in self.symbol:
                self._mostrar()
            else:
                self._ocultar()

    def mostrar_fav(self, fav_actived, filtro):
        if fav_actived:
            if self.is_favorite:
                if filtro.upper() in self.symbol:
                    self._mostrar()
                else:
                    self._ocultar()
            else:
                self._ocultar()

    def mostrar_margin(self, margin_actived, filtro):
        if margin_actived:
            if self.is_margin:
                self._mostrar()
            else:
                self._ocultar()
        else:
            self._mostrar()

    def toggle_favorite(self):
        item = Markets.get_symbol_by_exchange(self.text(), self.exchange)
        item.toggle_fav()
        self.setIcon(self._get_icon())

# ────────────────────────────────────────────────────────────────────────────────
