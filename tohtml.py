import os
import shutil
import sys

class HtmlWriter:
    def __init__(self, name):
        self.name=name
        os.chdir(name)
        os.makedirs("html/files",exist_ok=True)
    def work(self):
        with open('text/data.list') as f, open("html/index.html","w") as f2:
            self.names=f.read().splitlines()
            lenth = len(self.names)
            f2.write("<html><head><b>%s</b></head><body>"%self.name)
            for i in range(lenth):
                self.transform(i,lenth)
                f2.write('<p><a href="files/%d.html">%s</a></p>'%(i,self.names[i]))
            f2.write("</body></html")
    def transform(self,lineno,lenth):
        with open("text/files/%s.txt"%self.names[lineno],
                  encoding='utf-8') as f,open("html/files/%d.html"%lineno,'w',
                                              encoding='utf-8') as f2:
            f2.write("""<html>
<head><a><b>%s</b></a></head>
<body>\n"""%self.names[lineno])
            for i in f:
                f2.write("<p>%s<p>\n"%(i.rstrip()))
            
            f2.write("<p>")
            if lineno>0:
                f2.write('<a href="%d.html">上一章<a>'%(lineno-1))
            else:
                f2.write('<a>   </a>')
            f2.write('<a href="../index.html"> 目录 </a>')
            if lineno<lenth-1:
                f2.write('<a href="%d.html">下一章</a>'%(lineno+1))
            f2.write("</body></html")

