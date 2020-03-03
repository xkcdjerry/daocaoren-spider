# 输入一个稻草人书屋书名 e.g zhongjidouluo
# 就会爬出来它底下的所有书并存在一个文件夹里
# 转化为html或电子书我以后实现
import collections
import os
import sys
import re
import threading
import time

import bs4
import requests

Data = collections.namedtuple("Data", ("url", "name"))

FIREFOXHEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;\
q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;\
q=0.5,en-US;q=0.3,en;q=0.2",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) \
Gecko/20100101 Firefox/73.0"}

#速度：狼图腾：39章，8.18章每秒
#      终极斗罗：918章，12.94章每秒
def get(url):
    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]
    url = "http://" + url.lstrip("/")
    req = requests.get(url,headers=FIREFOXHEADERS)
    req.raise_for_status()
    req.encoding = 'utf-8'
    return req.text


def getsoup(url):
    return bs4.BeautifulSoup(get(url), "html.parser")


class Parser:
    SELECTER = 'div[id="all-chapter"] a[href][title][target="_blank"]'

    def __init__(self, url):
        self.soup = getsoup(url)

    def iter_tags(self):
        for i in self.soup.select(self.SELECTER):
            yield Data(i.get("href"), i.get("title"))


class Spider:
    def __init__(self, name, foldname):
        self.base_url = "www.daocaorenshuwu.com/book/%s/" % name
        self.name = name
        self.foldname = foldname
        self.p = Parser(self.base_url)
        self.lock=threading.Lock()

    def download_page(self, url, name):
        soup = getsoup(url)
        with open("files/%s.txt" % name, "w", encoding="utf-8") as f:
            # 写第一页
            writecontent(soup, f)

            # 选择出里面的页面列表
            pages = soup.select_one('ul[class="pagination pagination-sm"]')

            # 选择并写除了第一页之外的每一页
            for i in pages.select("li a[href]"):
                f.write("\n\n")
                writecontent(getsoup("%s%s" % (self.base_url, i.get("href"))),
                             f)
        
        with self.lock:
            print("已下载 %s" % name)
    def init(self):
        os.makedirs(self.foldname + '/text', exist_ok=True)
        os.chdir(self.foldname + "/text")
        os.makedirs("files",exist_ok=True)
    def work(self):
        threads=[]
        chapters = self.p.iter_tags()
        print("已抓取章节列表")
        with open('index.html', 'w') as f, open("data.list", "w") as f2:
            f.write("<html><body>")
            f.write("<head><b>%s</b></head>" % self.name)
            for i, data in enumerate(chapters, start=1):
                th=threading.Thread(target=self.download_page,
                                    args=(data.url, data.name))
                th.start()
                threads.append(th)
                f2.write(data.name + '\n')
                f.write('<p><a href="files/{0}.txt">{0}</a></p>\n'.format(data.name))
                f.flush()
                f2.flush()
            f.write("</html></body>")
        return threads

    def spider(self):
        self.init()
        start=time.time()
        threads=self.work()
        for i in threads:
            i.join()
        end=time.time()
        print("Downloaded %d chapters in %.2f seconds, On an average of %.2f \
per second"%(len(threads), end-start, len(threads)/(end-start)))

def write_content(soup, f):
    for i in soup.select("p"):
        if len(i.findParents()) == 6:# 分离出文字标签
            remove_spam(i)
            f.write(i.getText())

def remove_spam(tag):
    for i in tag.findChildren():
        i.extract()  # 把干扰项删掉


def main():
    if len(sys.argv)==1 or len(sys.argv)>3:
        sys.stderr.write("Usage: %s book_name [folder_name]"%sys.argv[0])
        raise SystemExit
    elif len(sys.argv)==2:
        Spider(sys.argv[1],sys.argv[1]).spider()
    elif len(sys.argv)==3:
        Spider(sys.argv[1],sys.argv[2]).spider()
    else:
        assert False,"Unreachable"


if __name__ == "__main__":
    main()
