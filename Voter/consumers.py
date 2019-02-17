from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class UpdateConsumer(JsonWebsocketConsumer):
    # noinspection PyAttributeOutsideInit
    def connect(self):
        self.user = self.scope["user"]
        # Don't accept anonymous users
        if self.user == 'AnonymousUser':
            self.close()
            return

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            'update',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            'update',
            self.channel_name
        )
        self.close()

    def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))
        # print(content)

        self.send_json(content)

    def update_full(self, event):
        self.send_json(
            {
                'type': 'update.full',
                'content': event['content']
            }
        )
