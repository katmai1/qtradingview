import logging
from PyQt5 import QtCore
# import notify2
from PyQt5.QtCore import QCoreApplication as qapp

from models.markets import Alarms


class CheckAlarms(QtCore.QThread):

    def run(self):
        self.sleep(10)
        for alarm in Alarms.select():
            if alarm.check_condition():
                mensaje = qapp.tr("Las condiciones de la alarma se han cumplido")
                logging.info(mensaje)
                self.notify(mensaje, alarm)
                if alarm.autodelete:
                    Alarms.delete_by_id(alarm.id)

    def notify(self, mensaje, alarm):
        logging.info(f"#{alarm.id} | {alarm.market.symbol}: {mensaje}")
        # notify2.init("QTradingView")
        # n = notify2.Notification(
        #     qapp.tr("Alarma!"),
        #     f"#{alarm.id} | {alarm.market.symbol}: {mensaje}",
        #     "logo.png"
        # )
        # n.show()

# ────────────────────────────────────────────────────────────────────────────────
