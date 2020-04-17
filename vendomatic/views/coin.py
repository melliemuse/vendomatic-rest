from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vendomatic.models import Coin


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for coin

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Coin
        url = serializers.HyperlinkedIdentityField(
            view_name='coin',
            lookup_field='id'
        )
        fields = ('id', 'coin')


class Coins(ViewSet):
    """coin"""

    def update(self, request, pk=None):
        """
        Handles PUT requests for individual Coin
        Returns:
            Response -- Custom Header with total coins and 204 status code
        """

        coin = Coin.objects.get(pk=pk)

        try:
            if coin:
                coin.coin += 1
        except:
            pass
        

        coin.save()

        return Response(headers={'X-coins': coin.coin}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """
        Handles DELETE request to individual Coin resource
        Returns:
            Response -- JSON serialized detail of deleted Coin
        """
        
        try:
            coin = Coin.objects.get(pk=pk)
            coin.delete()
            return Response(headers={'Coins to be returned': coin.coin -2}, status=status.HTTP_204_NO_CONTENT)

        except Coin.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 