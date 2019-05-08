# import socket, threading
# import time


# def tcplink(sock, addr):
#     print('Accept new connection from %s:%s...' % addr)
#     sock.send(b'Welcome!')
#     while True:
#         data = sock.recv(1024)
#         time.sleep(1)
#         if not data or data.decode('utf-8') == 'exit':
#             break
#         sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
#     sock.close()
#     print('Connection from %s:%s closed.' % addr)


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # 监听端口:
# s.bind(('127.0.0.1', 9999))

# s.listen(5)
# print('Waiting for connection...')

# while True:
#     # 接受一个新连接:
#     sock, addr = s.accept()
#     # 创建新线程来处理TCP连接:
#     t = threading.Thread(target=tcplink, args=(sock, addr))
#     t.start()

"""from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1> Hello, %s!</h1>' %(environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]

httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
httpd.serve_forever()"""

from flask import Flask
from flask import request
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == '' or password == '':
        return '<h3>Bad username or password.</h3>'
    conn = mysql.connector.connect(user='root', password='jiwenjie48', database='test')
    cursor = conn.cursor()
    cursor.execute('select * from login where username = %s', (username, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if username == result[0][0] and password == result[0][1]:
        return '<h3>Hello, admin</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == "__main__":
    app.run()