req_json_chrome = b"""GET /json HTTP/1.1\r
Host: 192.168.1.3:8080\r
Connection: keep-alive\r
Cache-Control: max-age=0\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36\r
DNT: 1\r
Accept-Encoding: gzip, deflate, sdch\r
Accept-Language: en-US,en;q=0.8\r\n\r\n"""

req_wiki_curl = b"""GET /wiki HTTP/1.1\r
Range: bytes=100-200\r
User-Agent: curl/7.41.0\r
Host: raptor:8080\r
Accept: */*\r\n\r\n"""

req_json_ie = b"""GET /json HTTP/1.1\r
Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*\r
Accept-Language: en-US,en;q=0.5\r
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)\r
Accept-Encoding: gzip, deflate\r
Host: raptor:8080\r
DNT: 1\r
Connection: Keep-Alive\r\n\r\n"""

req_json_iphone = b"""GET /json HTTP/1.1\r
Host: raptor:8080\r
Connection: close\r
Accept-Encoding: gzip, deflate\r
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4\r
Accept-Language: en-us\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n\r\n"""

import async

finished = async.prewait(async.object())

class HttpClient:
    initial_bytes_to_send = req_json_chrome

    def __init__(self):
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.count = 0
        self.func = self.first

    def first(self, transport, data):
        async.debug('first\n')
        self.data1 = data
        #async.debugbreak()
        self.func = self.second
        return req_json_ie

    def second(self, transport, data):
        async.debug('second\n')
        self.data2 = data
        self.func = self.third
        return req_json_iphone

    def third(self, transport, data):
        async.debug('third\n')
        #async.debugbreak_on_next_exception()
        self.data3 = data
        transport.close()
        async.signal(finished)
        #async.signal(transport)

    def data_received(self, transport, data):
        async.debug("data received!\n%s\n" % data)
        self.count += 1
        async.debug("count: %d\n" % self.count)
        retval = self.func(transport, data)
        async.debug('sending: %s\n' % retval)
        return retval
        #return self.func(transport, data)

def c1():
    c = async.client(async.IPADDR, 8080)

def _c():
    c = async.client(async.IPADDR, 8080)
    #async.prewait(c)
    async.register(transport=c, protocol=HttpClient)
    async.wait(finished)
    return c
