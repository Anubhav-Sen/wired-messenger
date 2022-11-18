import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    """
    This class defines the chat consumer.
    """
    def connect(self):
        """
        This function handels connections to the socket.
        """
        self.accept()

        self.send(text_data=json.dumps({
            'type':'connected',
            'message': 'you are connected'
        }))

    def disconnect(self, close_code):
        """
        This function handels disconnects from the socket.
        """
        pass

    def receive(self, text_data):
        """
        This function handels the data through the socket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))