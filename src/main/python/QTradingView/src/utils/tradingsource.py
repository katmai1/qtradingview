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
            # self.extract_nuevo(raw)

    def extract_nuevo(self, raw):
        # for i, div in enumerate(raw):
        #     print(f"{i}: {div.text}")
        ...

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

    # @property
    # def data_is_ok(self):
    #     raw = self.soup_find_class("pane-legend-title__description")
    #     if raw is None:
    #         return False
    #     if ":" in raw:
    #         return False
    #     return True

    def clear(self):
        self.market = None
        self.interval = None
        self.exchange = None
        self.html = None

    # @property
    # def titulo(self):
    #     try:
    #         return self.soup.title.string
    #     except Exception as e:
    #         print(e)
    #         return None

    # @property
    # def full_symbol(self):
    #     try:
    #         for script in self.soup.find_all("script"):
    #             if "editchart.model.symbol" in script.text:
    #                 raw = str(script.text).split('"editchart.model.symbol":')[1].split(',')[0]
    #                 return raw.replace('"', '')
    #     except Exception as e:
    #         print(e)
    #         return None

    # @property
    # def exchange(self):
    #     try:
    #         return self.full_symbol.split(":")[0].lower()
    #     except Exception as e:
    #         print(e)
    #         return None

    # @property
    # def symbol(self):
    #     try:
    #         return self.full_symbol.split(":")[1]
    #     except Exception as e:
    #         print(e)
    #         return None
