import socket


host = '127.0.0.1'
port = 2000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print('服务器监启动，端口为:{}...'.format(port))
s.listen(5)
print('服务器监听已启动...')

# socket服务器端固定套路，socket.socket --> bind --> listen --> accept

while True:
    connection, addr = s.accept()
    print('客户端{}已连接'.format(addr))

    raw_request = connection.recv(1024)
    request = raw_request.decode('utf-8')
    print('ip and request, {}\n{}'.format(addr, request))
    connection.sendall('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
                       '<h3>Hello world!</h3>'.encode('utf-8'))
    connection.close()
