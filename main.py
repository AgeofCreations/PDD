
import requests
from bs4 import *
from lxml import html
import xlrd, xlwt
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    import sys
    sys.excepthook = log_uncaught_exceptions

class PageDownload():
    def __init__(self, urls):
        self.urls = urls

    def taking_things(self):
        i = 1
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Output')

        ws.write(0, 0, 'URL')
        ws.write(0, 1, 'Title')
        ws.write(0, 2, 'Description')
        ws.write(0, 3, 'h1')
        ws.write(0, 4, 'Text')
        ws.write(0, 5, 'PFS(bottom)')
        ws.write(0, 6, 'PFS(upper)')

        for url in self.urls:
            try:
                self.s = requests.get(url)
                b = BeautifulSoup(self.s.content,"lxml")
                self.title = b.title.string
                self.desc1 = b.find(attrs={"name" : "description"})
                self.desc = self.desc1.get('content')
                self.h1 = b.h1.string
                self.text1 = b.find(attrs={"class" : "sl-description-text"})
                self.text = self.text1.contents
                self.sfp = b.find(attrs={"class" : "filter-pages-wrapper bottom"})
                self.sfpu = b.find(attrs={"class" : "top-filter-pages"})

            except Exception as e:
                e = 'Invalid URL'
                self.title = e
                self.desc = e
                self.h1 = e
                self.text = e

            print('Сейчас выполняется '+str(i)+'-й элемент списка из ' + str(len(self.urls))+'-х')

            self.xl_title = str(self.title)
            self.xl_desc = str(self.desc)
            self.xl_h1 = str(self.h1)
            self.xl_text = str(self.text)
            self.xl_sfp = str(self.sfp)
            self.xl_sfpu = str(self.sfpu)

            ws.write(i, 0, url)
            ws.write(i, 1, self.xl_title)
            ws.write(i, 2, self.xl_desc)
            ws.write(i, 3, self.xl_h1)
            ws.write(i, 4, self.xl_text)
            ws.write(i, 5, self.xl_sfp)
            ws.write(i, 6, self.xl_sfpu)

            i += 1

        wb.save(r'''C:\Users\kotov_or\PycharmProjects\PageDataDownloader\xl\output.xls''')

with open(r'''C:\Users\kotov_or\PycharmProjects\PageDataDownloader\xl\urloidi.txt''') as f:
    urls = f.read().splitlines()

p = PageDownload(urls)
p.taking_things()

