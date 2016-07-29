import threading


class GUIThread(threading.Thread):

    def __init__(self, process, func):
        """
        A thread used to run GUI in parallel

        :param CrawlerProcess process: Process of Scrapy that scrapes the Web for songs
        :param func: The function to run when the thread is started.
        """
        threading.Thread.__init__(self)
        self.process = process
        self.func = func

    def run(self):
        self.func(self.process)


class DownloadThread(threading.Thread):
    def __init__(self, func):
        """
        A thread used for downloading Audio files

        :param func: The function that is run in the thread.
        """
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()
