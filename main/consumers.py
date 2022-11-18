import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    """
    This class defines the chat consumer.
    """
    def connect(self):
        """
        This function handels connections to the socket.
        """
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = 'chat_%s' % self.chat_id
        self.session_user = self.scope['session']['user_data'] or None
        self.session_token = self.scope['session']['token_key'] or  None

        if self.session_token and self.session_user:

            async_to_sync(self.channel_layer.group_add)(self.chat_name, self.channel_name) 
            self.accept()

        else:
            self.close()

    def disconnect(self, close_code):
        """
        This function handels disconnects from the socket.
        """
        async_to_sync(self.channel_layer.group_discard)(self.chat_name, self.channel_name)

    def receive(self, text_data):
        """
        This function handels the data through the socket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        async_to_sync(self.channel_layer.group_send)(self.chat_name, {'type': 'chat_message', 'message': message, 'user_data': self.session_user})

    def chat_message(self, event):
        """
        This function sends the chat message it received.
        """
        message = event['message']
        user_data = event['user_data']

        self.send(text_data=json.dumps({'message': message, 'user_data': user_data}))