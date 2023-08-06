import requests
from urllib.parse import urlencode, unquote

name = "requests_from_file"


class requestFactory():
    params = None

    def __init__(self, headerFileName, contentFileName=None):
        headerFile = open(headerFileName, "r", encoding="utf-8")
        headerLines = headerFile.readlines()
        headerFile.close()
        self.params = dict()

        line0 = headerLines[0]
        headers = dict()
        # 处理Method
        self.params["method"] = line0.split()[0]
        href = line0.split()[1]
        # Headers里加载了所有的数据
        for line in headerLines[1:]:
            map = line.split(":", 1)
            headers[map[0]] = map[1].strip()

        # 取出其中的Cookie
        self.params['cookies'] = None
        if 'Cookie' in headers:
            from http.cookies import SimpleCookie
            cookie = SimpleCookie(headers['Cookie'])
            cookies = {i.key: i.value for i in cookie.values()}
            self.params['cookies'] = cookies
            headers.pop('Cookie')

        # 取出其中的Json
        self.params['json'] = None
        if 'Json' in headers:
            self.params['json'] = headers['Json']
            headers.pop('Json')

        # 去除Headers中的多余信息
        if 'Content-Type' in headers:
            headers.pop('Content-Type')
        if 'Content-Length' in headers:
            headers.pop('Content-Length')

        # headers作为params的一部分了
        self.params['headers'] = headers

        # 拼凑出Url
        href_split = href.split("?")
        href = href_split[0]
        param_list = href_split[1]
        params_dictory = {}
        for param in param_list.split("&"):
            keyV = param.split("=")
            key = keyV[0]
            value = unquote(keyV[1])
            params_dictory[key] = value
        self.params['params']  = params_dictory

        httpHeader = 'http://'
        if 'Referer' in headers and 'https' in headers['Referer']:
            httpHeader = 'https://'
        self.params['url'] = httpHeader + headers['Host'] + href

        # 加载Post的data
        self.params['data'] = None
        if contentFileName is not None:
            contentFile = open(contentFileName, "r", encoding="utf-8")
            contentLines = contentFile.readlines()
            contentFile.close()
            content = dict()
            for contentline in contentLines:
                map = contentline.split("=", 1)
                if len(map)<2:
                    map.append("")
                content[map[0]] = map[1].strip()
            self.params['data'] = content


    def request(self):
        params = self.params
        # r = requests.request(params['method'],params['url'],
        #                      cookies=params['cookies'],
        #                      headers=params['headers'],
        #                      json=params['json'],
        #                      data=params['data'])
        r = requests.request(**params)
        return r

    def build(self):
        params = self.params
        return requests.Request(**params)
