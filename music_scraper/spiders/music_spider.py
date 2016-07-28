import cgi

import scrapy

from music_scraper.gui import GUI

items = []


def is_standard_website(href):
    if 'google' not in href and 'youtube' not in href and 'twitter' not in href and 'facebook' not in href:
        return True
    else:
        return False


class MusicSpider(scrapy.Spider):
    name = "music"

    def parse(self, response):
        for href in response.xpath("//a/@href").extract():
            if href[:7] == '/url?q=' and is_standard_website(href):
                url = href[7:].split('&')[0]
                yield scrapy.Request(url, meta={'download_maxsize': 2097152}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//a/@href').extract():
            url = response.urljoin(sel)
            yield scrapy.Request(url, method='HEAD', callback=self.parse_final_contents)

    def parse_final_contents(self, response):
        if response.headers['Content-Type'].decode('UTF-8') == 'audio/mpeg':
            _, params = cgi.parse_header(response.headers.get('Content-Disposition', '').decode('UTF-8'))
            filename = params['filename']
            while True:
                if GUI.url_dict.get(filename) is None:
                    GUI.url_dict[filename] = response.url
                    GUI.size_dict[filename] = int(response.headers['Content-Length'].decode('UTF-8'))
                    break
                else:
                    split_file = filename.split('.')
                    filename = ''.join(split_file[:-1] + ['_.'] + split_file[-1:])
            GUI.strings += [filename]
            GUI.refresh_values()
            GUI.update_screen()
