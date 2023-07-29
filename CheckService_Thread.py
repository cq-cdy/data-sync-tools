import threading
import xml.dom.minidom as xml
import FinalTest.InitService as s

"""
A separate thread ensures that the JVM based service listener is turned on
"""


class Service_Thread(threading.Thread):

    def run(self):
        ini_information = {}
        dom = xml.parse("properties/service.xml")
        root = dom.documentElement
        itemlist = root.getElementsByTagName('entry')
        for db in itemlist:
            ini_information['host'] = db.getElementsByTagName('host')[0].childNodes[0].data
            ini_information['port'] = db.getElementsByTagName('port')[0].childNodes[0].data
            ini_information['user'] = db.getElementsByTagName('user')[0].childNodes[0].data
            ini_information['password'] = db.getElementsByTagName('password')[0].childNodes[0].data
            ini_information['db'] = db.getElementsByTagName('db')[0].childNodes[0].data
            ini_information['check'] = db.getElementsByTagName('service-check')[0].childNodes[0].data
        if str.upper(ini_information.get("check")) == "TRUE":
            s._start_service_moniter(
                "properties/service_mode.data",
                ini_information.get('host'),
                int(ini_information.get('port')),
                ini_information.get('user'),
                ini_information.get("password"),
                ini_information.get("db")
            )
