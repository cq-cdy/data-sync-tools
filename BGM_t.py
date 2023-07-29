import threading
import xml.dom.minidom as xml


class BGM(threading.Thread):

    def run(self):
        ini_information = {}
        dom = xml.parse("properties/service.xml")
        root = dom.documentElement
        itemlist = root.getElementsByTagName('entry')
        for db in itemlist:
            ini_information['bgm'] = db.getElementsByTagName('bgm')[0].childNodes[0].data
        if str.upper(ini_information.get("bgm")) == "TRUE":
            import pygame
            file = r'music/bgm.MP3'
            pygame.mixer.init()
            music = pygame.mixer.music.load(file)
            while True:
                if pygame.mixer.music.get_busy() == False:
                    pygame.mixer.music.play()
