from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端向后端发送websocket连接请求时，自动触发
        # 服务端允许创建连接
        self.accept()

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接受消息
        print(message)
        self.send("websocket test")

    def websocket_disconnect(self, message):
        # 断开连接时，自动触发
        raise StopConsumer()
