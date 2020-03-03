import sys
import os

def main():
    if len(sys.argv)==2 and sys.argv[1]=="help":
        print("""
Usage: %s (spider|tohtml|to-one-file) bookname
options:
    spider: spider the given bookname, perducing program-usable and human-\
readable(though not pretty) files.
    tohtml: use the spidered content to create a html linked and indexed page \
that can be server with the command "python -m http.server" (The html's not \
perfect, I'm still working on it)
    to-one-file: (not made yet) (Use the spidered content and make it into one \
lage .txt file for easy coping and reading)


bookname: the name that appers in the last part in the url if you opened it\
in the browser(right after book)(e.g. langtuteng)
"""%os.path.basename(sys.argv[0]))
    elif len(sys.argv)==3:
        do, bookname=sys.argv[1:]
        if do=='spider':
            import spider
            spider.Spider(bookname).spider()
        elif do=="tohtml":
            import tohtml
            tohtml.HtmlWriter(bookname)
    else:
        sys.stderr.write("""Usage:
python {0} (spider|tohtml|to-one-file) bookname
                  or
python {0} help""".format(os.path.basename(sys.argv[0])))
        raise SystemExit

if __name__ == "__main__":
    main()
        
