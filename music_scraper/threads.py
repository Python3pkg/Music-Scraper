import threading


class GuiThread(threading.Thread):
    def __init__(self, process, func):
        threading.Thread.__init__(self)
        self.process = process
        self.func = func

    def run(self):
        self.func(self.process)


class DownloadThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()
