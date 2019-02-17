from channels.generic.websocket import JsonWebsocketConsumer


class UpdateConsumer(JsonWebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        self.accept() if user != 'AnonymousUser' else self.close()

    def disconnect(self, close_code):
        pass

    def receive_json(self, content, **kwargs):
        print(content)

        self.send_json(content)
