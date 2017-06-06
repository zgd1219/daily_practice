import socket

host = '127.0.0.1'
port = 2000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


# socket客户端, socket.socket --> connect

def get_response(s):
    response = b''
    while True:
        r = s.recv(1024)
        if len(r) == 0:
            break
        response += r
    return response


request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(host)
s.send(request.encode('utf-8'))
response = get_response(s)
print('response响应', response.decode('utf-8'))
