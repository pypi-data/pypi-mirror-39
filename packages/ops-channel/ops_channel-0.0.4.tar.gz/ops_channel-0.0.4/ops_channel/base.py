#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'xiaozhang'

import atexit
from signal import SIGTERM
import sys
import os
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
import urllib
if PY2:
    import urllib2 as urllib2
    import httplib
    from urlparse import urlparse
    import Queue as queue
    reload(sys)
    sys.setdefaultencoding('utf-8')

if PY3:
    import urllib.request as urllib2
    import queue as queue
    from urllib.parse import urlparse
    urllib.urlencode=urllib.parse.urlencode
    import http.client as httplib





import subprocess
import time
import datetime
import re
import logging
import hashlib
import base64

import tempfile
import threading
import getopt
from logging.handlers import RotatingFileHandler
import json
import random
import platform
import socket

import uuid
import inspect
import getpass

PLATFORM=platform.system().lower()
PYTHON_PATH='/usr/bin/python'

def init_log():
    dirs=['/tmp/','/var/','/etc/','/bin/','/var/log/']
    for d in dirs:
        if not os.path.exists(d):
            os.mkdir(d)
    user=getpass.getuser()
    client_log_filename='/var/log/cli.log'
    try:
        if PLATFORM!='windows':
            _p=os.popen('which python').read().strip()
            if _p!='' and len(_p)>0:
                PYTHON_PATH=_p
    except Exception as er:
        pass

    log_dir= os.path.dirname(client_log_filename)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    # if user=='root':
    #     os.chmod(log_dir,0666)
    log_fmt_str='%(asctime)-25s %(module)s:%(lineno)d  %(levelname)-8s %(message)s'
    if PY2:
        logging.basicConfig(level=logging.DEBUG,
                format=log_fmt_str,
                filemode='a+')
    if PY3:
        log_fmt_str='%(asctime)s %(module)s:%(lineno)d  %(levelname)s %(message)s'
        logging.basicConfig(level=logging.DEBUG,
                format=log_fmt_str)
    logger = logging.getLogger('CLI')
    file_handler=RotatingFileHandler(filename=client_log_filename,maxBytes=100 * 1024 * 1024, backupCount=3)
    formatter= logging.Formatter(log_fmt_str)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter )
    logger.addHandler(file_handler)
    if user=='root' and PLATFORM!='windows':
        try:
            if len(os.popen('command -v chattr').read())>1:
                os.popen('chattr -a %s'%(client_log_filename)).read()
                os.chmod(client_log_filename,766)
                # os.popen('chattr +a %s'%(client_log_filename)).read()
        except Exception as er:
            pass
    try:
        os.chmod(client_log_filename, 766)
    except Exception as er:
        pass
    return logger

logger=init_log()
log=logger

class ZbxCommon(object):
    def __init__(self):
        self.machine_id=''
        self.config={}

    def urlencode(self,str):
        reprStr=repr(str).replace(r'\x','%')
        return reprStr[1:-1]

    def get_product_uuid(self):
        if self.machine_id!='' and len(self.machine_id)==36:
            return self.machine_id
        product_uuid=''
        # if os.path.isfile('/sys/devices/virtual/dmi/id/product_uuid'):
        #     product_uuid=self.execute('cat /sys/devices/virtual/dmi/id/product_uuid').strip()
        if product_uuid=="":
            uuid_file='/etc/machine_id'
            if not os.path.exists(uuid_file):
                product_uuid=self.get_uuid()
                with open(uuid_file,'w') as file:
                    file.write(product_uuid)
            else:
                with open(uuid_file,'r') as file:
                    product_uuid=file.read()
        self.machine_id=product_uuid
        return product_uuid

    def get_basic_auth(self,user='',pwd=''):
        s=user.strip()+':'+pwd.strip()
        if PY2:
            return 'Basic '+ base64.encodestring(s).strip()
        if PY3:
            return 'Basic ' + str(base64.encodestring(s.encode('utf-8')),'utf-8').strip()

    def _download(self,filename,directory,filepath):
        try:
            data={'file':filename,'dir':directory}
            data=urllib.urlencode(data)
            if filename.startswith('http://') or filename.startswith('https://'):
                http_url=filename
                if http_url.endswith('/'):
                    http_url=http_url[0:len(http_url)-1]
                if http_url.rindex('/')>0 and http_url.rindex('/')<len(http_url):
                    filename=http_url[http_url.rindex('/')+1:]
                filename=filename.replace('?','')
                filepath=filename
            else:
                http_url = '%s/%s/download?%s' % (server_url, default_module, data)
            def _download(url,data,filepath):
                #logger.info('download file url:%s'%(str(url)))
                request = urllib2.Request(url)
                request.add_header('User-Agent', 'CLI(1.0)')
                if filename.startswith('http://') or filename.startswith('https://'):
                    request.add_header('auth-uuid', self._get_config('auth-uuid'))
                conn = urllib2.urlopen(request)
                f = open(filepath,'wb')
                f.write(conn.read())
                f.close()
            _download(http_url,data,filepath)
            try:
                line=''
                with open(filepath, 'r') as _file:
                    if PY3:
                        try:
                            _file.readline().encode()
                        except Exception as er:
                            pass
                    else:
                        line=str(_file.readline()).strip()
                if line.startswith('redirect:http://') or line.startswith('redirect:https://'):
                    _download(line,data,filepath)
            except Exception as er:
                print('(error) %s' % (str(er)))
                logger.error(er)
        except Exception as e:
            logger.error(e)
            print('(error) %s'%(str(e)))

    def _upload(self,url,filepath,directory):
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)
        fr=open(filepath,'rb')
        filename=os.path.basename(filepath)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'filename')
        data.append(filename)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'dir')
        data.append(directory)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('file',filename))
        data.append('Content-Type: %s\r\n' % 'image/png')

        if PY3:
            http_body = "\r\n".join(data)+'\r\n'
            from io import BytesIO, StringIO
            f = BytesIO()
            f.write(http_body.encode(encoding="utf-8"))
            f.write(fr.read())
            f.write(('\r\n--%s--\r\n' % boundary).encode(encoding="utf-8"))
        else:
            data.append(fr.read())
            data.append('--%s--\r\n' % boundary)
            http_body = '\r\n'.join(data)
        fr.close()


        try:
            if PY3:
                req=urllib2.Request(url, data=f.getvalue())
            else:
                req = urllib2.Request(url, data=http_body)
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            req.add_header('User-Agent','Mozilla/5.0')
            req.add_header('Referer','http://remotserver.com/')
            req.add_header('auth-uuid',self._get_config('auth-uuid'))
            resp = urllib2.urlopen(req, timeout=5)
            qrcont=resp.read()
            print(qrcont.decode())
        except Exception as e:
            logger.error(e)
            print('(error)%s'%(str(e)))


    def url_fetch_witherr(self,url,data=None,header={},timeout=30,httpCmd=''):
        return self._url_fetch(url,data=data,header=header,timeout=timeout,httpCmd=httpCmd)

    def get(self,url,timeout=30):
        return self._url_fetch(url,timeout=timeout)

    def post(self,url,data=None,header={},timeout=30):
        return self._url_fetch(url, data=data, header=header, timeout=timeout)

    def url_fetch(self,url,data=None,header={},timeout=30,httpCmd='',debug=False):
        try:
            return self._url_fetch(url,data=data,header=header,timeout=timeout,httpCmd=httpCmd,debug=debug)
        except Exception as er:
            #logger.error('url_fetch error:%s'+str(er))
            print(er)
            return ''

    def _get_config(self,key):
        home= os.path.expanduser('~')
        fn=home+'/.cli'
        content=''
        data={}
        try:
            if os.path.isfile(fn):
                with open(fn) as f:
                    content=f.read()
                    content=str(content).strip()
                lines=re.split(r'\n',content)
                for line in lines:
                    line=line.strip()
                    pos=line.find('=')
                    if pos>0:
                        data[line[0:pos]]=line[pos+1:]
                if len(data)>0:
                    self.config=data
        except Exception as er:
            logger.error(er)
        if key in self.config.keys():
            return self.config[key]
        else:
            return ''

    def _set_config(self,key,value):
        home= os.path.expanduser('~')
        fn=home+'/.cli'
        kv=[]
        ks=['token','auth-uuid']
        for _k in  ks:
            if not _k in self.config.keys():
                self.config[_k]=''
        self.config[key]=value
        for k,v in self.config.items():
            kv.append('%s=%s'%(k,v))
        try:
            if os.path.isfile(fn):
                with open(fn,'w') as f:
                    f.write("\n".join(kv))
                return True
            else:
                try:
                    with open(fn, 'w') as f:
                        f.write("\n".join(kv))
                except Exception as e:
                    logger.error(e)
        except Exception as er:
            logger.error(er)
            return False

    def _url_fetch(self,url,data=None,header={},timeout=30,httpCmd='',debug=False):
        html=''
        handle=None
        machine_id=self.get_product_uuid()
        key= self._get_config('auth-uuid')
        try:
            headers = {
                'User-Agent':'CLI agent(1.0)',
                'auth-uuid':key,
                'token':self._get_config('token'),
                'machine-id':machine_id,
            }
            if len(header)>0:
                for k,v in header.items():
                    headers[k]=v
            if data!=None:
                data=urllib.urlencode(data)
                if PY3:
                    data=data.encode('utf-8','ignore')
                # print(data)

            req = urllib2.Request(
                url =url,
                headers = headers,
                data=data
            )
            if httpCmd != "":
                req.get_method = lambda: httpCmd

            handle=urllib2.urlopen(req,timeout=timeout)



            html=handle.read()
            cm=r'<meta[^>]*charset=[\'\"]*?([a-z0-8\-]+)[\'\"]?[^>]*?>'
            if PY3:
                cm=cm.encode('utf-8','ignore')
            charset=re.compile(cm,re.IGNORECASE).findall(html)
            if len(charset) >0:
                if charset[0]=='gb2312':
                    charset[0]='gbk'
                if PY2:
                    html=unicode(html,charset[0])
            if PY3:
                return html.decode('utf-8','ignore')
        except Exception as e:
            raise Exception(e)
        finally:
            if handle!=None and handle.fp!=None:
                try:
                    handle.fp.close()
                except Exception as er:
                    pass

        return html

    def _cmdline_args(self,s):
        import re
        s = re.subn(r'\\"', '{,,}', s)[0]
        s = re.subn(r"\\'", '{,}', s)[0]
        l = re.findall(r"'[^']+?'|\"[^\"]*?\"", s, re.IGNORECASE | re.MULTILINE)
        # l= re.findall(r"'[\s\S]*[\']?'|\"[\s\S]*[\"]?\"",s,re.IGNORECASE|re.MULTILINE)
        for i,v in enumerate(l):
            s=s.replace(v,'{'+str(i)+'}')
        p=re.split(r'\s+',s)
        ret=[]
        def repl(a):
            i=re.findall(r'\{\d+\}', a.group(0))
            a =  re.sub('\{\d+\}',  l[int(re.sub(r'^{|}$', '', i[0]))],a.group(0))
            return a

        for a in p:
            # print a
            i = re.findall(r'\{\d+\}', a)
            if len(i)>0:
                a=re.sub(r'[\s\S]+',repl,a)
            if re.match(r"'[\s\S]+'",a) or re.match(r'"[\s\S]+"',a):
                a=re.sub("^'|'$|^\"|\"$",'',a)
            a = re.subn(r"\{\,\,\}", '\"', a)[0]
            a = re.subn(r"\{\,\}", "\'", a)[0]
            ret.append(a)
        return ret

    def getopt(self,inputs):
        if isinstance(inputs,basestring):
            inputs=self._cmdline_args(inputs)

        def ptype(input):
            if input == "":
                return (0,"")
            if "-" == input[0] and len(input) == 2:
                return (1,input[1])
            if "--" == input[:2] and len(input) >= 4:
                return (2,input[2:])
            return (0,"")
        def istype(input):
            if len(input) <= 0:
                return 0
            if "-" == input[0]:
                return 1
            return 0
        ret = {}
        u = 0
        ucount = len(inputs)
        icount = 0
        ls = []
        if ucount >= 1:
            while 1:
                if u >= ucount:
                    break
                if istype(inputs[u]) == 1:
                    break

                ls.append(inputs[u])
                u += 1

            inputs = inputs[u:]
            icount = len(inputs)

        if icount >= 1:
            i = 0
            state = 0
            while 1:
                t,name = ptype(inputs[i])
                for c in range(1):
                    if t == 0 :
                        i += 1
                        break
                    if i+1 < icount:
                        tt,tname = ptype(inputs[i+1])
                        if tt != 0:
                            ret[name] = ""
                            i += 1
                            break
                        ret[name] = inputs[i+1]
                        i += 2
                        break
                    ret[name] = ""
                    i += 1
                    break
                if i >= icount:
                    break
        return (ret)

    def parse_argv(self,argv):
        data={}
        long_args=[]
        short_args=[]
        for v in argv:
            if v.startswith('--'):
                long_args.append(v.replace('--','')+"=")
            elif v.startswith('-'):
                short_args.append(v.replace('-',''))
        opts= getopt.getopt(argv,":".join(short_args)+":",long_args)
        for opt in opts[0]:
            data[opt[0].replace('-','')]=opt[1]
        if len(data)>0:
            return data
        else:
            return argv

    def md5(self, src):
        m2 = hashlib.md5()
        if PY3:
            src=str(src).encode('utf-8','ignore')
        m2.update(src)
        return m2.hexdigest()

    def now_datetime(self):
        now_datetime = time.strftime('_%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        return now_datetime

    def _date_format(self,fmt):
        return  time.strftime(fmt, time.localtime(time.time()))

    def date(self,fmt='%Y-%m-%d'):
        return self._date_format(fmt)

    def time(self,fmt='%H:%M:%S'):
        return self._date_format(fmt)

    def now(self,fmt='%Y-%m-%d %H:%M:%S'):
        return self._date_format(fmt)

    def match(self, s, m, o='ima'):
        flags = 0
        is_all = False
        for i in range(0, len(o)):
            if o[i] == 'i':
                flags = flags | re.IGNORECASE
            if o[i] == 'm':
                flags = flags | re.MULTILINE
            if o[i] == 'a':
                is_all = True
        r = re.compile(m, flags=flags)
        ret = r.findall(s)
        if is_all:
            return json.dumps(ret)
        if len(ret) > 0:
            return ret[0]
        else:
            return ''

    def execute(self,cmd,timeout=30):
        try:
            return ZbxCommand(cmd).run(timeout=timeout)
            # return os.popen(cmd).read()
        except Exception as err:
            logger.error(err)
            return ""


    def get_all_ip_list(self):
        if platform.system().lower()=='windows':
            name,xx,ips=socket.gethostbyname_ex(socket.gethostname())
            return ips
        else:
            # cmdline = "ip a | egrep \"^\s*inet.*\" | grep -v inet6 | awk '{print $2}' | awk -v FS='/' '{print $1}'"
            cmdline = "ip a"
            ret = self.execute(cmdline)
            ips= re.findall(r'inet\s*(\d+\.\d+\.\d+\.\d+)',ret)
            if len(ips)==0:
                return [self._get_host_ip()]
            else:
                return ips
            # lip=re.split(r'\n',ret)
            # ips=[]
            # for ip in lip:
            #     if str(ip).strip ()!='':
            #       ips.append(ip.strip())
            # return ips


    def get_uuid(self):
        return str(uuid.uuid4())

    def uuid(self):
        return self.get_uuid()

    def jq(self,data, key, pretty=False):
        return self._get_json(data,key,pretty=False)

    def _get_json(self,data, key, output='text', sep=' ', quote='', pretty=False):
        def parse_dict(data, key):
            return data.get(key, None)

        def parse_list(data, key):
            ret = []
            if re.match(r'^\d+$', key):
                return data[int(key)]

            for i in range(0, len(data)):
                if isinstance(data[i], dict):
                    if key == '*':
                        for j in data[i].keys():
                            ret.append(data[i].get(j, None))
                    else:
                        ret.append(data[i].get(key, None))
                elif isinstance(data[i], list):
                    for j in range(0, len(data[i])):
                        if key == '*':
                            ret.append(data[i][j])
                        else:
                            ret.append(data[i][j].get(key, None))

            return ret

        if key.find(',') != -1:
            ks = key.split(',')
        else:
            ks = key.split('.')

        for k in ks:
            if isinstance(data, list):
                data = parse_list(data, k)
                # print(k,data)
            elif isinstance(data, dict):
                data = parse_dict(data, k)
                # print(k,data)
        return data

    def _get_host_ip(self):
        ip='127.0.0.1'
        s=None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            try:
                if s!=None:
                    s.close()
            except Exception as er:
                pass
        return ip

    def ip(self):
        return self._get_host_ip()


    def replace(self, s, o, n):
        ret = re.subn(re.compile(o, re.MULTILINE | re.IGNORECASE), n, s)
        if len(ret) > 0:
            return ret[0].strip()
        else:
            return s.strip()

    def join(self, s,  sep=',',wrap='',trim_null=True):
        if isinstance(s, list):
            if trim_null:
                t = []
                for i in s:
                    if isinstance(i, str) or isinstance(i, unicode):
                        if i.strip() == '':
                            continue
                    if i == None:
                        continue
                    t.append(i)
                s = t
            if wrap != '':
                s = ['%s%s%s' % (wrap, str(i), wrap) for i in s]
            return sep.join(s)
        return s

    def split(self, s, sep,trim_null=True):
        ret= re.split(re.compile(sep, re.MULTILINE | re.IGNORECASE), s)
        rets=[]
        if trim_null:
            for i in ret:
                if str(i).strip()=='':
                    continue
                else:
                    rets.append(i)
        else:
            return ret
        return rets

    def rand(self):
        return random.random()

    def randint(self,min=1,max=100):
        return random.randint(min,max)

    def json_encode(self,obj):
        return json.dumps(obj)

    def json_decode(self,s):
        return json.loads(s)

    def format_shell_str(self,strs):
        return strs.replace('\\','\\\\').replace('"','\\\"')

    def format(self,strs,dict_param,is_shell_str=False):
        m=re.findall(r"{\w+}|\:\w+",strs,re.IGNORECASE|re.DOTALL)
        v=list()
        def lcmp(x,y):
            if len(x)>len(y):
                return -1
            else:
                return 1
        for i in m:
            key,num=re.subn(r"^'?\{|\}'?$|^\:",'',i)
            if is_shell_str:
                strs = strs.replace(i, self.format_shell_str(dict_param[key]))
            else:
                strs=strs.replace(i,dict_param[key])
        return strs


    def randstr(self,length=10):
        seq=[chr(x) for x in range(65,91)]
        ret=[]
        i=length
        while i>0:
            i=i-1
            ret.append(seq[random.randint(0,len(seq)-1)])
        return ''.join(ret)


    def help(self):
        h='''
        # from ops_channel import cli #导入包
        # cli.get('http://www.bb.com',timeout=2) #get获取网页，返回网页内容，注意错误处理
        # cli.post('http://test.web.com',{'name':'jqzhang'},timeout=2) #post获取网页 返回网页内容，注意错误处理
        # cli.execute('hostname',timeout=2) #执行命令
        # cli.join(['a','b','c'],sep=',') #数组并接，返回字符串
        # cli.jq({'data':{'rows':[{'id':1,'name':'hello'},{'id':2,'name':'world'}]}},'data,rows') #json 获取
        # cli.match('hello123world456','\d+') #正则匹配，返回数组
        # cli.split('hello123world456','\d+') #正则分割，返回数组
        # cli.getopt("cli api -u root --sudo 1 --token abc -c 'hostname' -t 5 ") #命令行参数获取，返回字典
        # cli.rand() #随机数，返回浮点数
        # cli.randint(1,100) #随机数，两者之间
        # cli.randstr(20) #随机字符串
        # cli.format('sadf {name} xxx',{'name':'jqzhang'}) #格式化，入参数为(str,dict) 返回字符串
        # data=cli.execute('cli status')
        # print( cli.execute( cli.format('echo "{json}"|cli jq -k count',{'json':data},is_shell_str=True))) #python 与 shell交互
        '''
        print(h)


    def get_hostname(self):
        os_name = os.name
        host_name = ""
        try:
            if os_name == 'nt':
                host_name = os.getenv('computername')
            elif os_name == 'posix':
                host = os.popen('hostname')
                try:
                    host_name = host.read().strip()
                except:
                    host_name=''
                finally:
                    host.close()
            if host_name.strip()=='':
                host_name= socket.gethostbyname()
        except Exception as er:
            logger.error(er)
            return ""
        return host_name.strip()

    def _is_alive(self,port, address='127.0.0.1'):
        port = int(port)
        import socket
        s = socket.socket()
        try:
            s.settimeout(5)
            s.connect((address, port))
            return True
        except Exception as er:
            return False
        finally:
            try:
                s.close()
            except Exception as er:
                pass
    def check_port(self,port,address='127.0.0.1'):
        return self._is_alive(port,address)

    def _exec_filename(self):
        path = os.path.realpath(sys.path[0])
        if os.path.isfile(path):
            path = os.path.dirname(path)
            return os.path.abspath(path)+ os.path.sep+__file__
        else:
            caller_file = inspect.stack()[1][1]
            return os.path.abspath(os.path.dirname(caller_file))+ os.path.sep+__file__



    def tuple2list(self,*args):
        print(args)
        l=[]
        for i in args:
            l.append(i)
        return l

    def command_args(self,args):
        if isinstance(args,list) or isinstance(args,tuple):
            return '"%s"' % '" "'.join(args)
        else:
            return str(args)


class ZbxCommand(object):
    def __init__(self, cmd,is_log='0'):
        mc=re.match('^su\s+[\'"a-zA-z09]+?\s+\-c',cmd)
        if PLATFORM=='windows' and mc!=None:
            cmd=cmd.replace(mc.group(0),'')
            cmd=cmd.strip()
            cmd=re.sub('^\"|\"$','',cmd)
        self.cmd = cmd
        self.process = None
        self.is_log=is_log
        self.return_code=-1
        self.util=ZbxCommon()
        self.messge_success=''
        self.message_error=''
        self.uuid=str(datetime.datetime.now()).replace(' ','').replace(':','').replace('-','').replace('.','')
        self.uuid_error=self.uuid+'error'
        self.result=open(tempfile.gettempdir()+ os.path.sep +self.uuid,'a+')
        self.result_error=open(tempfile.gettempdir()+ os.path.sep +self.uuid_error,'a+')


    def run(self, timeout=30,task_id='', url_success='',url_error='',url='',ip=''):
        def feedback(url,result,task_id,return_code=0,ip=''):
            try:
                machine_id=self.util.get_product_uuid()
                if ip=='':
                    ip=self.util.get_one_ip()
                data=self.util.url_fetch_witherr(url,{ 'cmd':self.cmd,'machine_id':machine_id,'result':result,'task_id':task_id,
                'success':self.messge_success,'error':self.message_error,'return_code':return_code,'ip':machine_id,'s':self.util.get_hostname(),'i':ip},timeout=8)
                if PY2:
                    if isinstance(data,str):
                        logger.info('feedback result:%s'+ str(data))
                    if isinstance(data,unicode):
                        logger.info('feedback result:%s' + str(data.encode('utf-8','ignore')))
                if PY3:
                    if isinstance(data,str):
                        logger.info('feedback result:%s'+ str(data))
            except Exception as er:
                data={'task_id':task_id,'result':result,'url':url}
                logger.error('feedback error:\t'+str(er)+json.dumps(data))


        def target():
            if self.is_log=='1':
                logger.info("task_id:%s"%(task_id)+"\t"+str(self.cmd))
            elif self.is_log=='2':
                logger.info("task_id:%s" % (task_id) + "\t cmd:mask")

            self.process = subprocess.Popen(self.cmd, shell=True,stdout=self.result,stderr=self.result_error)
            self.process.communicate()
            self.process.poll()
            self.return_code = self.process.returncode
            if self.return_code==None:
                self.return_code=-1
        thread = threading.Thread(target=target)
        thread.start()
        if timeout==-1:
            thread.join()
        thread.join(timeout)




        def get_result():
            result=''
            error=''
            try:
                result= open(tempfile.gettempdir()+ os.path.sep+self.uuid,'r').read()
                if self.is_log=='1':
                    logger.info("task_id:%s\tSuccess Result:" %(task_id) + str(result))
                elif self.is_log=='2':
                    logger.info("task_id:%s\tSuccess Result:mask" % (task_id))
                elif self.is_log=='3':
                    logger.info("task_id:%s\tSuccess Result:" % (task_id) + str(result))
            except Exception as er:
                print(self.cmd)
                print('get_result:\t'+str(er))
                logger.error(er)
            finally:
                try:
                    self.result.close()
                    os.unlink(tempfile.gettempdir()+ os.path.sep+self.uuid)
                except Exception as er:
                    print('get_result:\t' + str(er))
                    logger.error(er)
                    pass
            try:
                error = open(tempfile.gettempdir() + os.path.sep + self.uuid_error, 'r').read()
            except Exception as err:
                logger.error(er)
                print(err)
                if self.is_log == '1' or self.is_log == '2' or self.is_log == '3':
                    logger.error("task_id:%s\tException Result:" % (task_id) + str(error))
            finally:
                try:
                    self.result_error.close()
                    os.unlink(tempfile.gettempdir() + os.path.sep + self.uuid_error)
                except Exception as er:
                    print('get_result close :\t' + str(er))
                    logger.error(er)

            return result.strip(),error.strip()
        if thread.is_alive():
            logger.warn(self.cmd)
            result, error = get_result()
            if url != '':
                feedback(url, result, task_id, self.return_code,ip)
            if url_error!='':
                feedback(url_error, "(error)timeout\n%s"%(str(result)+str(error)), task_id, -1,ip)
                if self.is_log == '1' or self.is_log == '2' or self.is_log == '3':
                    logger.info("task_id:%s\ttimeout result has feedback to url:%s result:%s error:%s" % (task_id,url_error,result,error))
            else:
                logger.info('timeout task_id:%s' % (task_id))
            self.process.terminate()
            thread.join()
            if result!='':
                return "(error)timeout \nresult:%s error:%s" % (str(result), str(error))
                #return result
            return "(error)timeout \nresult:%s error:%s" % (str(result), str(error))
            #util.url_fetch(server_url+'/slowlog',{'param':{ 'cmd':self.cmd,'ip':util.get_one_ip()}})
        result,error= get_result()
        try:
            if re.findall(r'\(error\)\s+file\s+not\s+found', result):
                self.return_code=127
        except Exception as er:
            pass

        self.messge_success=result
        self.message_error=error

        if result=='' and error!='':
            result='finish'
        if url!='':
            feedback(url, result, task_id, self.return_code,ip)
            if self.is_log=='1' or self.is_log=='2' or self.is_log=='3':
                logger.info("task_id:%s\t result has feedback to url:%s "%(task_id,url))
        if  self.return_code==0 and url_success!='':
            feedback(url_success,result,task_id,self.return_code,ip)
            if self.is_log=='1' or self.is_log=='2' or self.is_log=='3':
                logger.info("task_id:%s\tsuccess result has feedback to url:%s "%(task_id,url_success))
        if self.return_code!=0 and url_error!='':
            feedback(url_error,result,task_id,self.return_code,ip)
            if self.is_log=='1' or self.is_log=='2' or self.is_log=='3':
                logger.info("task_id:%s\terror result has feedback to url:%s " % (task_id,url_error))
        if error.strip()!='':
            return result+"\n"+error
        else:
            return result


cli=ZbxCommon()



# from ops_channel import cli
# cli.get('http://www.bb.com',timeout=2)
# cli.post('http://test.web.com',{'name':'jqzhang'},timeout=2)
# cli.execute('hostname',timeout=2)
# cli.join(['a','b','c'],sep=',')
# cli.jq({'data':{'rows':[{'id':1,'name':'hello'},{'id':2,'name':'world'}]}},'data,rows')
# cli.match('hello123world456','\d+')
# cli.split('hello123world456','\d+')
# cli.getopt("cli api -u root --sudo 1 --token abc -c 'hostname' -t 5 ")
# cli.rand()
# cli.randint(1,100)
# cli.randstr(20)
# print(cli.format('sadf {name} xxx',{'name':'jqzhang'}))
# data=cli.execute('cli status')
# print( cli.execute(  cli.format('echo "{json}"|cli jq -k count',{'json':data},is_shell_str=True)))
# cli.help()

