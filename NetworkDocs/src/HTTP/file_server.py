import re
import socket


def send_2_client(tcp_client):
    # 向客户端发送数据
    recv = tcp_client.recv(1024).decode()
    recv = recv.splitlines()  # ['GET / HTTP/1.1', 'Host: 192.168.1.101:8080', 'Connection: keep-alive', ...]

    # 获取请求内容
    if recv:
        methods = None
        ret = None
        try:
            methods = re.match("^(.+?)\s", str(recv[0]))
            methods = methods.group(0).strip()
            ret = re.match("[^/]+(/[^ ]*)", str(recv[0]))
            ret = ret.group(1).strip()
        except Exception as e:
            print(e.args)

        if ret:
            print("当前文件目录", ret)
            headers = "HTTP/1.1 200 OK\r\n"

            try:
                with open("TestFile" + ret, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(e.args)
                content = ""

            if content:
                headers += "Content-Disposition: attachment;filename={}\r\n\r\n".format(ret.strip("/"))
                headers += content
            else:
                headers += "content-type: text/html;charset=utf-8\r\n\r\n"
                headers += "文件不存在"

            tcp_client.send(headers.encode("utf-8"))

        print("{}-请求响应完毕....".format(tcp_client))

    tcp_client.close()


def main():
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 绑定本地ip
    sock.bind(("192.168.1.101", 8080))

    # 开启监听
    sock.listen(128)

    while True:
        # 处理客户端连接
        response_client, response_address = sock.accept()

        try:
            send_2_client(response_client)
        except Exception as e:
            print(e.args)
            break

    # 关闭套接字
    sock.close()


if __name__ == '__main__':
    main()
