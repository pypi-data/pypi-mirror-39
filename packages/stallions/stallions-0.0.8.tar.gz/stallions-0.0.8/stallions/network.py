import requests
import random

HTTP_DEFAULT_TIMEOUT = 8
BROWSER_USER_AGENT = [
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
]


class HtmlFetcher(object):
    def __init__(self):
        self.http_timeout = HTTP_DEFAULT_TIMEOUT
        # set header
        self.headers = {'User-agent': random.choice(BROWSER_USER_AGENT)}

    @staticmethod
    def get_encoding_type(apparent_encoding, html_encoding_list):
        #  utf-8 < GB2312、BIG5、GBK、GB18030
        html_encoding = ''
        if len(html_encoding_list) > 0:
            html_encoding = html_encoding_list[0]
        data_list = [apparent_encoding, html_encoding]
        gbk_list = [x for x in data_list if "GB" in x.upper()]
        if len(gbk_list) > 0:
            return gbk_list[0]
        utf_list = [x for x in data_list if "UTF" in x.upper()]
        if len(utf_list) > 0:
            return utf_list[0]
        return 'UTF-8'

    def get_html(self, url, coding=True):
        # do request
        html = ''
        try:
            req = requests.get(url, headers=self.headers, timeout=self.http_timeout)
            header = req.headers
            # 剔除二进制
            content_type = header.get('Content-type', None)
            if content_type == 'application/octet-stream':
                return html
            response_encoding_list = requests.utils.get_encodings_from_content(req.text)
            # print(req.headers['content-type'])
            # print("response内容的encoding编码:", req.encoding)
            # print("response headers里设置的apparent_encoding编码:", req.apparent_encoding)
            # print("response返回的html header标签里设置的编码:", response_encoding_list)
            # print(req.status_code)
            if coding:
                print(req.encoding, req.apparent_encoding, response_encoding_list)
            if req.encoding == "ISO-8859-1":
                req.encoding = self.get_encoding_type(req.apparent_encoding, response_encoding_list)
            req.keep_alive = False
            return req.text
            # print(html)
        except Exception as e:
            print(e, "encoding error")
        # print(html, 'html')
        return html


class FileFetcher(object):
    @staticmethod
    def get_html(url):
        # do read
        print(url)
        try:
            with open(url, "r", encoding="utf-8") as file_obj:
                html = file_obj.read().strip()
        except Exception as e:
            print(e)
            html = None
        return html
