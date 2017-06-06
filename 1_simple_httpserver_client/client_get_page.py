'''
功能实现:
给一个网页url，抓取下载整个网页，类似requests.get的功能
例如抓取豆瓣电影top250，https://movie.douban.com/top250
底层通过socket，熟悉http的请求和响应内容，更好理解网页抓取的原理
步骤思路:
1.解析url，解析出protocol，host，port，path
2.根据protocol(http,https)建立socket(ssl_socket)
3.通过socket连接访问url并得到网站的response响应
4.解析响应，得到响应状态码、响应header、响应body
5.保存body内容，即网站页面

'''

import socket
import ssl


def parsed_url(url):
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    i = u.find('/')
    if i == -1:
        path = '/'
        host = u
    else:
        host = u[:i]
        path = u[i:]

    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        print('host and port', h)
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    return s


def reponse_by_socket(s):
    response = b''
    while True:
        r = s.recv(1024)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ', 1)
        headers[k] = v
    return status_code, headers, body


# 把上面的过程封装到get函数
def get(url):
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    s.send(request.encode('utf-8'))

    response = reponse_by_socket(s)
    r = response.decode('utf-8')

    status_code, headers, body = parsed_response(r)
    if status_code in [301, 302]:
        url = headers['Location']
        return  get(url)
    return status_code, headers, body


# 测试函数, 测试url解析的是否正确
def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]

    for t in test_items:
        url, expect = t
        print('url', url)
        u = parsed_url(url)
        e = '解析失败, ({}) ({}) ({})'.format(url, u, expect)
        assert u == expect, e
        print('{}解析成功,结果为{}'.format(url, expect))


def main():
    url = 'http://www.zgd666.cc/topic/'
    status_code, headers, body = get(url)
    print(status_code, headers, body)


if __name__ == '__main__':
    main()


