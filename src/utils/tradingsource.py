from bs4 import BeautifulSoup
from time import sleep


class TradingSource:
    '''clase per extreure dades de la pagina de tradingview'''

    def __init__(self):
        self.clear()

    def read_html(self, html):
        self.html = html
        raw = self.soup_find_class("pane-legend-title__description")
        if raw is None:
            print("No se ha cargado la pagina correctamente")
        else:
            if ":" in raw:
                self.extract_data_2()
            else:
                self.extract_data_1()
    
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
            return soup.find(class_=clase).text
        except Exception as e:
            print("Error al fer el soup!")
            print(e)
            return None
    
    @property
    def data_is_ok(self):
        raw = self.soup_find_class("pane-legend-title__description")
        if raw is None:
            return False
        if ":" in raw:
            return False
        return True

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