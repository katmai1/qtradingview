from bs4 import BeautifulSoup
import logging


class TradingSource:
    '''clase per extreure dades de la pagina de tradingview'''

    def __init__(self):
        self.clear()

    def read_html(self, html):
        self.html = html
        raw = self.soup_find_class("legend-source-title")
        if raw is None:
            logging.debug("No se ha cargado la pagina correctamente")
        else:
            self.market = raw[0].text
            self.interval = raw[1].text
            self.exchange = raw[2].text
 
    def extract_data_1(self):
        self.market = self.soup_find_class("pane-legend-title__description")
        self.interval = self.soup_find_class("pane-legend-title__interval")
        self.exchange = self.soup_find_class("pane-legend-title__details")

    def extract_data_2(self):
        raw = self.soup_find_class("pane-legend-title__description")
        self.exchange, self.market = raw.split(":")
        self.interval = self.soup_find_class("pane-legend-title__interval")

    def soup_find_class(self, clase):
        try:
            soup = BeautifulSoup(self.html, 'html5lib')
            return soup.findAll('div', {"data-name" : clase})
        except AttributeError:
            ...
            return None
        except Exception as e:
            logging.error("Fallo al filtrar con BeautifulSoup")
            logging.error(e.__str__())
            return None

    def clear(self):
        self.market = None
        self.interval = None
        self.exchange = None
        self.html = None
