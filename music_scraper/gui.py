import curses
try:
    from urllib import request
except ImportError:
    import urllib2 as request

from math import ceil

from music_scraper.threads import DownloadThread


class GUI:

    size_dict = {}
    url_dict = {}
    screen = None
    status = 'Scraping Music ... It might take some time.'
    strings = []
    pages = 0
    page = 1
    position = 1
    max_row = 0
    row_num = 0
    box = None
    high_light_text = None
    normal_text = None
    key = None
    run_download = False
    gui_stopped = False

    @staticmethod
    def init_display():
        if not GUI.gui_stopped:
            curses.noecho()
            curses.cbreak()
            curses.start_color()
            GUI.screen.keypad(1)
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
            GUI.high_light_text = curses.color_pair(1)
            GUI.normal_text = curses.A_NORMAL
            curses.curs_set(0)
            GUI.refresh_values()
            GUI.position = 1
            GUI.page = 1
            GUI.box = curses.newwin(GUI.max_row + 3, curses.COLS, 0, 0)
            GUI.box.addstr(1, 1, GUI.status, GUI.high_light_text)
            GUI.add_bottom_menus()
            GUI.screen.refresh()
            GUI.box.refresh()

    @staticmethod
    def refresh_values():
        if not GUI.gui_stopped:
            GUI.max_row = curses.LINES - 3
            GUI.row_num = len(GUI.strings)
            GUI.pages = int(ceil(GUI.row_num / GUI.max_row))

    @staticmethod
    def add_bottom_menus():
        GUI.box.addstr(curses.LINES - 1, 0, "ESC:Exit", GUI.high_light_text)
        GUI.box.addstr(curses.LINES - 1, curses.COLS // 2, "ENTR:Download", GUI.high_light_text)

    @staticmethod
    def on_key_down():
        if GUI.page == 1:
            if GUI.position < min(GUI.max_row, GUI.row_num):
                GUI.position += 1
            else:
                if GUI.pages > 1:
                    GUI.page += 1
                    GUI.position = 1 + (GUI.max_row * (GUI.page - 1))
        elif GUI.page == GUI.pages:
            if GUI.position < GUI.row_num:
                GUI.position += 1
        else:
            if GUI.position < GUI.max_row + (GUI.max_row * (GUI.page - 1)):
                GUI.position += 1
            else:
                GUI.page += 1
                GUI.position = 1 + (GUI.max_row * (GUI.page - 1))

    @staticmethod
    def on_key_up():
        if GUI.page == 1:
            if GUI.position > 1:
                GUI.position -= 1
        else:
            if GUI.position > (1 + (GUI.max_row * (GUI.page - 1))):
                GUI.position -= 1
            else:
                GUI.page -= 1
                GUI.position = GUI.max_row + (GUI.max_row * (GUI.page - 1))

    @staticmethod
    def on_key_left():
        if GUI.page > 1:
            GUI.page -= 1
            GUI.position = 1 + (GUI.max_row * (GUI.page - 1))

    @staticmethod
    def on_key_right():
        if GUI.page < GUI.pages:
            GUI.page += 1
            GUI.position = (1 + (GUI.max_row * (GUI.page - 1)))

    @staticmethod
    def on_key_enter():
        thread = DownloadThread(GUI.download_item)
        thread.start()

    @staticmethod
    def display_list():
        for i in range(1 + (GUI.max_row * (GUI.page - 1)), GUI.max_row + 1 + (GUI.max_row * (GUI.page - 1))):
            if GUI.row_num == 0:
                GUI.box.addstr(1, 1, GUI.status, GUI.high_light_text)
            else:
                if i + (GUI.max_row * (GUI.page - 1)) == GUI.position + (GUI.max_row * (GUI.page - 1)):
                    GUI.box.addstr(i - (GUI.max_row * (GUI.page - 1)), 2, str(i) + " - " + GUI.strings[i - 1],
                                   GUI.high_light_text)
                else:
                    GUI.box.addstr(i - (GUI.max_row * (GUI.page - 1)), 2, str(i) + " - " + GUI.strings[i - 1],
                                   GUI.normal_text)
                if i == GUI.row_num:
                    break

    @staticmethod
    def update_screen():
        if not GUI.gui_stopped:
            if GUI.key == curses.KEY_DOWN:
                GUI.on_key_down()
            elif GUI.key == curses.KEY_UP:
                GUI.on_key_up()
            elif GUI.key == curses.KEY_LEFT:
                GUI.on_key_left()
            elif GUI.key == curses.KEY_RIGHT:
                GUI.on_key_right()
            if GUI.key == ord("\n") and GUI.row_num != 0:
                GUI.on_key_enter()

            GUI.box.erase()
            GUI.display_list()
            GUI.add_bottom_menus()
            GUI.screen.refresh()
            GUI.box.refresh()

    @staticmethod
    def update_on_key():
        if not GUI.gui_stopped:
            GUI.key = GUI.screen.getch()
            while GUI.key != 27 or GUI.run_download:
                if ord('c') == GUI.key or ord('C') == GUI.key:
                    GUI.run_download = False
                GUI.update_screen()
                GUI.key = GUI.screen.getch()
            curses.endwin()

    @staticmethod
    def download_item():
        if GUI.run_download or GUI.gui_stopped:
            return
        GUI.run_download = True
        filename = GUI.strings[GUI.position - 1]
        url = GUI.url_dict[filename]
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        u = request.urlopen(req)
        f = open(filename, 'wb')

        file_size_dl = 0
        block_sz = 8192
        while GUI.run_download:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = "Downloading " + filename + " [%3.2f%%]" % (file_size_dl * 100. / GUI.size_dict[filename])
            GUI.box.erase()
            GUI.box.addstr(0, 0, status, GUI.high_light_text)
            GUI.box.addstr(curses.LINES - 1, 0, "C:Cancel Download", GUI.high_light_text)
            GUI.screen.refresh()
            GUI.box.refresh()

        f.close()
        GUI.run_download = False
        GUI.key = curses.KEY_DOWN
        GUI.update_screen()
