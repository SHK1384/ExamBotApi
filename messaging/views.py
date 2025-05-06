from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .models import Message

from .serializers import MessageSerializers, UpdateMessageSentBoolSerializer

# Create your views here.


class MessagingView(ViewSet):
    def get_all_messages(self, request):
        messages = Message.objects.all()
        serialized_output = MessageSerializers(messages, many=True)
        return Response(serialized_output.data, status=status.HTTP_200_OK)

    def set_message_sent_bool(self, request):
        serialized_output = UpdateMessageSentBoolSerializer(data=request.data)
        if serialized_output.is_valid(raise_exception=True):
            message = Message.objects.get(pk=serialized_output['message_id'])
            message.is_sent = True
            message.save()
            return Response({'message': 'Done!'}, status=status.HTTP_200_OK)
