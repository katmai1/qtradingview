import logging

from PyQt5.QtWidgets import QStyledItemDelegate, QListWidgetItem, QStyleOptionViewItem, QMenu, QAction
from PyQt5.QtGui import QIcon

from qtradingview.models.markets import Markets


class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QStyleOptionViewItem.Right
        super(CustomItemDelegate, self).paint(painter, option, index)


class CustomContextMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mw = self.parent().parent().parent().parent()  # ref a mainwindow

    def handler(self, position):
        self._item = self._get_item(position)
        if self._item is not None:
            self._insert_favorite(self._item)
            self._insert_actions(self._item)
            self.exec_(self.parent().mapToGlobal(position))

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────
    # devuelve el item seleccionado o devuelve None si no lo hay
    def _get_item(self, position):
        try:
            return self.parent().itemAt(position)
        except Exception as e:
            logging.warning("Exception trying get item on this position.")
            logging.error(e.__str__())
            return None

    # funcion para configurar las opciones rapidamente
    def _action(self, texto, cmd, icono=None, shortcut=None):
        action = QAction(texto, self, triggered=cmd)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icono is not None:
            action.setIcon(QIcon(icono))
        return action

    # inserta los menus que ejecutan eventos
    def _insert_actions(self, item):
        self.addAction(self._action(self.tr("Load chart..."), self._run_load_chart, icono=":/actions/markets", shortcut="Return"))
        self.addSeparator()
        self.addAction(self._action(self.tr("Add to portfolio..."), self._run_add_portfolio, icono=":/actions/portfolio"))
        self.addAction(self._action(self.tr("New alarm..."), self._runNewAlarm, icono=":/actions/alarms"))
        self.addSeparator()
        self.addAction(self._action(self.tr("Set as initial market"), self._run_set_initial_market, icono=":/actions/settings"))

    # inserta menu favorito, ejecuta evento externo
    def _insert_favorite(self, item):
        v = {}
        v[True] = {"txt": self.tr("Remove from favorite"), "ico": ":base/voidstar"}
        v[False] = {"txt": self.tr("Add to favorite"), "ico": ":base/star"}
        self.addAction(self._action(v[item.is_favorite]['txt'], item.toggle_favorite, shortcut="Esc", icono=v[item.is_favorite]['ico']))

    # ─── EVENTS ────────────────────────────────────────────────────────────────────

    def _runNewAlarm(self):
        self.mw.dock_alarms.addAlarm(self._item.exchange, self._item.symbol)

    def _run_load_chart(self):
        self.mw.load_chart(self._item.symbol, self._item.exchange)

    def _run_set_initial_market(self):
        self.mw.config['initial_exchange'] = self._item.exchange.title()
        self.mw.config['initial_market'] = self._item.symbol
        self.mw.ctx.save_config()

    def _run_add_portfolio(self):
        self.mw.dock_portfolio.addPortfolio(self._item.exchange, self._item.symbol)

# ────────────────────────────────────────────────────────────────────────────────

# ─── ITEMS ──────────────────────────────────────────────────────────────────────


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

    #
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
