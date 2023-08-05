import sys,os,socket
from . import web4 as web
from os import path
# from base64 import b64encode,b64decode
from yxspkg import encrypt
# from urllib.parse import quote, unquote
sys.argv.append('8088')
urls = (   
    '/f/.*','FileSystem',
    '/download/.*','download',
    '/video/.*','video')
file_render=web.template.render(path.split(__file__)[0],cache=False)
urlset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
urlset += urlset.lower()
urlset += '0123456789'
urlset = urlset.encode('utf8')
def encode(url):
    # return(quote(url))
    return encrypt.spencode(url.encode('utf8'),passwd='jiami',str_set=urlset).decode('utf8')
def decode(url):
    # return(unquote(url))
    return encrypt.spdecode(url.encode('utf8'),passwd='jiami',str_set=urlset).decode('utf8')

class FileSystem:
    def GET(self,*d):
        url=web.url()[3:]
        print('first',url)
        url=decode(url)
        if not url:
            p=os.getcwd()+os.sep
        elif path.isdir(url):
            p=url
        else:
            print('url raise',encode(url))
            raise web.seeother('/download/file?f1='+encode(url))
            return
        x=os.listdir(p)
        a=[]
        for i in x:
            filename=p+i
            if path.isfile(filename):
                a.append([filename,i])
            else:
                a.append([filename+os.sep,i+os.sep])
        a.sort(key=lambda x:x[1][-1])
        a.insert(0,[path.split(p[:-1])[0]+os.sep,'..'])
        for i in a:
            i[0]='/f/'+encode(i[0])
        # return file_render.w126()
        print(p)
        return file_render.file(a,path.split(p[:-1])[1])
    def POST(self):
        url=web.url()[3:]
        filedir=decode(url)
        x = web.input()
        if not filedir:filedir='./'
        if True: # to check if the file-object is created
            fname = path.join(filedir,path.basename(x['file_name']))
            print(fname)
            fout = open(fname,'wb') # creates the file where the uploaded file should be stored
            fout.write(x['file_content'])
            fout.close() # closes the file, upload complete.
        raise web.seeother(url)

class video:
    def GET(self,*d):
        s='''
        <!DOCTYPE HTML>
<html>
<body>

<video controls autoplay>
<source src="/static/gsd/live.m3u8" type="application/vnd.apple.mpegurl" />
<p class="warning">your not support</p>
</video>

</body>
</html>'''
        return s
def download_file(fp,length,file_name='package'):
    BUF_SIZE=1024*1024
    try:
        web.header('Content-Type','application/octet-stream')
        web.header('Content-disposition', 'attachment; filename={name}'.format(name=file_name))
        web.header('Content-Length',str(length))
        while True:
            c = fp.read(BUF_SIZE)
            if c:
                yield c
            else:
                break
    except Exception as err:
        print(err)
        yield 'Error'
    finally:
        if fp:
            fp.close()
class download:
    def GET(self):
        t=web.input()
        file_list=list(t.values())
        print(len(file_list))
        url=file_list[0]
        print('source  ',url)
        file_name=decode(url)
        file_path = path.join('file_path', file_name)
        f = open(file_name, "rb")
        length=path.getsize(file_name)
        for i in download_file(f,length,path.basename(file_name)):
            yield i
def getip():
    return socket.gethostbyname(socket.gethostname())
def website():
    app=web.application(urls, globals())
    app.run()
if __name__ == '__main__': 
    x=getip()
    print('本机ip：{ip}'.format(ip=x))
    website()
