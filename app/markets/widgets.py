from PyQt5.QtWidgets import QStyledItemDelegate, QListWidgetItem, QStyleOptionViewItem, QMenu, QAction
from PyQt5.QtGui import QIcon, QKeySequence

from models.markets import Markets


class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QStyleOptionViewItem.Right
        super(CustomItemDelegate, self).paint(painter, option, index)


class CustomContextMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def handler(self, position):
        self._item = self.parent().itemAt(position)
        self._insert_load_chart()
        self._insert_favorite(self._item.is_favorite)
        self._insert_select_initial_market()
        self.exec_(self.parent().mapToGlobal(position))

    # funcion para configurar las opciones rapidamente
    def _action(self, icono, texto, cmd, shortcut=None):
        action = QAction(QIcon(icono), texto, self, triggered=cmd)
        if shortcut is not None:
            action.setShortcut(shortcut)
        return action

    # ─── INSERT MENUS ────────────────────────────────────────────────────────────────────
    def _insert_select_initial_market(self):
        self.addAction(self._action(":/actions/settings", "Set as initial market", self._run_set_initial_market))
        
    def _insert_load_chart(self):
        self.addAction(self._action(":/actions/markets", "Load chart...", self._run_load_chart, "Return"))

    # accion favorito toggle
    def _insert_favorite(self, fav):
        v = {}
        v[True] = {"txt": "Remove from favorite", "ico": ":base/voidstar"}
        v[False] = {"txt": "Add to favorite", "ico": ":base/star"}
        self.addAction(self._action(v[fav]['ico'], v[fav]['txt'], self._item.toggle_favorite, "Esc"))

    # ─── ACTIONS ────────────────────────────────────────────────────────────────────

    def _run_load_chart(self):
        self.parent().parent().parent().parent().load_chart(self._item.symbol, self._item.exchange)

    def _run_set_initial_market(self):
        self.parent().parent().parent().parent().config['initial_exchange'] = self._item.exchange.title()
        self.parent().parent().parent().parent().config['initial_market'] = self._item.symbol
        self.parent().parent().parent().parent().ctx.save_config()

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
