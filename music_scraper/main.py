import curses

try:
    from urllib import request
except ImportError:
    import urllib2 as request

from scrapy.crawler import CrawlerProcess

from music_scraper.gui import GUI
from music_scraper.threads import GuiThread
from music_scraper.spiders.music_spider import MusicSpider

try:
    input = raw_input
except NameError:
    pass


def start_gui(process):
    def create_ui(screen):
        GUI.screen = screen
        GUI.strings = []
        GUI.init_display()
        GUI.update_on_key()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        GUI.gui_stopped = True

    curses.wrapper(create_ui)
    process.stop()


def main():
    process = CrawlerProcess({'LOG_ENABLED': False})
    message = ''
    while message == '':
        message = input("Give me something to start with - (Example: kabali song download ) : ")
    s = request.quote(message)
    MusicSpider.start_urls = [
        "http://www.google.com/search?q=" + s,
    ]
    process.crawl(MusicSpider)
    thread = GuiThread(process, start_gui)
    thread.start()
    process.start()
    if len(GUI.strings) == 0 and not GUI.gui_stopped:
        GUI.box.erase()
        GUI.box.addstr(0, 0, "No Results Found... Try with Some other keywords.", GUI.high_light_text)
        GUI.box.addstr(curses.LINES - 1, 0, "ESC:Exit", GUI.high_light_text)
        GUI.box.addstr(curses.LINES - 1, curses.COLS // 2, "ENTR:Download", GUI.high_light_text)
        GUI.screen.refresh()
        GUI.box.refresh()
