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

    def _get_icon(self):
        if self.is_favorite:
            return QIcon(":/base/star.svg")
        return QIcon(":/base/voidstar.svg")

    def _mostrar(self):
        self.setHidden(False)

    def _ocultar(self):
        self.setHidden(True)

    def configurar(self, symbol, exchange):
        self.setText(symbol)
        self.exchange = exchange.lower()
        self.setIcon(self._get_icon())

    def mostrar(self, only_favorites, filtro):
        # mostrar nomes favoritos...
        if only_favorites:
            # si es favorito y passa el filtre es mostra
            if self.is_favorite:
                if filtro.upper() in self.symbol:
                    self._mostrar()
                # si no passa el filtre...
                else:
                    self._ocultar()
            # si no es favorite...
            else:
                self._ocultar()

        # sino esta clickat el buton favoritos...
        else:
            # y passa el filtro...
            if filtro.upper() in self.symbol:
                self._mostrar()
            else:
                self._ocultar()

    def toggle_favorite(self):
        item = Markets.get_symbol_by_exchange(self.text(), self.exchange)
        item.toggle_fav()
        self.setIcon(self._get_icon())

# ────────────────────────────────────────────────────────────────────────────────
