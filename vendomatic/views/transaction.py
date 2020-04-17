from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vendomatic.models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for transaction

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Transaction
        url = serializers.HyperlinkedIdentityField(
            view_name='transaction',
            lookup_field='id'
        )
        fields = ('id', 'beverageId', 'coin')


class Transactions(ViewSet):
    """transaction"""

    def update(self, request, pk=None):
        """
        Handles PUT requests for individual Message item
        Returns:
            Response -- Empty body with 204 status code
        """

        message = Message.objects.get(pk=pk)

        message.message_body = request.data["message_body"]
        message.logged_in_user_id = request.data["logged_in_user_id"]
        message.match_id = request.data["match_id"]

        message.save()


        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def create(self, request):
        """
        Handles POST request for Message
        Returns:
            Response JSON serialized Message instance
        """

        current_user = request.auth.user.dater.id

        message = Message()

        message.message_body = request.data["message_body"]
        message.logged_in_user_id = current_user
        message.match_id = request.data["match_id"]

        message.save()
        serializer=MessageSerializer(message, context={'request': request})

        return Response(serializer.data)