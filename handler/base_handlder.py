# _*_ encoding=utf-8 _*_


class BaseRequestHandler:
    def __init__(self,server,request,client_address):
        self.server = server
        self.request = request
        self.client_address = client_address

    # 这个函数逻辑是留给具体的业务逻辑去实现的
    def handle(self):
        pass

class StreamRequestHandler(BaseRequestHandler):
    def __init__(self,server,request,client_address):
        BaseRequestHandler.__init__(self,server,request,client_address)

        # 将读和写分成两个连接描述符
        self.rfile = self.request.makefile('rb')
        self.wfile = self.request.makefile('wb')
        self.wbuf = []

    # 编码：字符串->字节码
    def encode(self,msg):
        if not isinstance(msg,bytes):
            msg = bytes(msg,encoding='utf-8')
        return msg

    # 解码：字节码->字符串
    def decode(self,msg):
        if not isinstance(msg,bytes):
            msg = msg.decode()
        return msg

    # 读消息：需要知道读取的消息有多长
    def read(self,length):
        msg = self.rfile.read(length)
        return self.decode(msg)

    # 读取一行消息,一个http请求报文的最大长度是65536
    def readline(self,length=65536):
        msg = self.rfile.readline(length).strip()
        return self.decode(msg)

    #写消息：将消息写入缓存
    def write_content(self,msg):
        msg = self.encode(msg)
        self.wbuf.append(msg)

    # 发送消息
    def send(self):
        for line in self.wbuf:
            self.wfile.write(line)
        self.wfile.flush()
        self.wbuf = []

    def close(self):
        self.wfile.close()
        self.rfile.close()