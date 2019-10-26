from PyQt5 import QtWidgets, QtGui, QtCore
from ui.dock_markets_Ui import Ui_dock_markets
from db import db, Markets
from tasks.update_markets_db import UpdateMarkets_DB


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QtWidgets.QStyleOptionViewItem.Right
        super(ItemDelegate, self).paint(painter, option, index)


class CustomItem(QtWidgets.QListWidgetItem):

    exchange = None

    @property
    def symbol(self):
        return self.text()

    @property
    def is_favorite(self):
        return Markets.check_symbol_is_fav(self.symbol, self.exchange)

    def _get_icon(self):
        if self.is_favorite:
            return QtGui.QIcon(":/base/star.svg")
        return QtGui.QIcon(":/base/voidstar.svg")

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
        
# ────────────────────────────────────────────────────────────────────────────────


class DockMarkets(QtWidgets.QDockWidget, Ui_dock_markets):

    exchanges = ['binance', 'bitfinex']

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.parent = parent
        self.setupUi(self)

        #
        self._load_exchanges()
        self._signals()
        #
        self.delegate = ItemDelegate()
        self.list_markets.setItemDelegate(self.delegate)
        self.list_markets.installEventFilter(self)
        #
    
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.list_markets):
            menu = QtWidgets.QMenu()
            menu.addAction('Open Window')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
            return True
        return super(QtWidgets.QDockWidget, self).eventFilter(source, event)


    def _signals(self):
        self.combo_exchange.currentTextChanged.connect(self.onExchangeChanged)
        self.list_markets.itemDoubleClicked.connect(self.onDoubleClickMarket)
        # self.list_markets.mouseReleaseEvent = self.onClickMarket
        # self.list_markets.keyReleaseEvent = self.onKeyRelease
        self.edit_filtro.textEdited.connect(self.onFiltroChanged)
        self.btn_favorite.toggled.connect(self.onClickFavoriteButton)

    @property
    def selected_exchange(self):
        return self.combo_exchange.currentText().lower()

    @property
    def fav_is_checked(self):
        return self.btn_favorite.isChecked()

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    def onClickFavoriteButton(self, fav_actived):
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(fav_actived, filtro)

    def onFiltroChanged(self, text):
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.fav_is_checked, text)

    def onExchangeChanged(self):
        self.edit_filtro.clear()
        self._load_markets()

    def onActionActualizaMarkets(self):
        t = UpdateMarkets_DB(self)
        t.run()

    def onDoubleClickMarket(self, item):
        self.parent._load_chart(item.text(), self.selected_exchange)

    def onClickMarket(self, event):
        if event.button() == 2:
            item = self.list_markets.itemAt(event.pos())
            dbitem = Markets.get_symbol_by_exchange(item.text(), self.selected_exchange)
            dbitem.toggle_fav()
            item.setIcon(self._get_icon_by_symbol(item.text()))

    # def onKeyRelease(self, event):
    #     if event.key() == QtCore.Qt.Key_Space:
    #         print("espacio")

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _load_exchanges(self):
        """ Carga la lista de exchanges en el combo, selecciona el definido por defecto y llama al evento de cambio """
        self.combo_exchange.clear()
        for x in self.exchanges:
            path = f":/exchanges/{x}.png"
            self.combo_exchange.addItem(QtGui.QIcon(path), x.title())
        # initial config
        default_index = self.combo_exchange.findText(self.parent.initial_exchange.title())
        if default_index != -1:
            self.combo_exchange.setCurrentIndex(default_index)
        # load markets
        self.onExchangeChanged()

    def _load_markets(self):
        filtro = self.edit_filtro.text()
        self.list_markets.clear()
        for it in Markets.get_all_by_exchange(self.selected_exchange):
            nuevo = CustomItem(self.list_markets)
            nuevo.configurar(it.symbol, self.selected_exchange)
            nuevo.mostrar(self.fav_is_checked, filtro)

# ────────────────────────────────────────────────────────────────────────────────
