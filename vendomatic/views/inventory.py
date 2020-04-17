from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vendomatic.models import Beverage, Coin

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


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for inventory

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    coin = CoinSerializer
    class Meta:
        model = Beverage
        url = serializers.HyperlinkedIdentityField(
            view_name='inventory',
            lookup_field='id'
        )
        fields = ('id', 'stock')


class Inventories(ViewSet):
    """inventory"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for inventory item

        Returns:
            Response -- JSON serialized inventory instance
        """
        try:
            beverage = Beverage.objects.raw(
            '''
            SELECT bev.id as id, bev.quantity as quantity, COUNT(trans.beverageId_id) as sold, (bev.quantity - COUNT(trans.beverageId_id)) AS stock FROM
            vendomatic_beverage bev
            LEFT Join vendomatic_transaction trans
            on bev.id = trans.beverageId_id
            GROUP BY trans.beverageId_id;
            '''
        )
            serializer = InventorySerializer(beverage[int(pk)-1], context={'request': request})
            return Response({'Remaining Item Quantity': beverage[int(pk)-1].stock})
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to inventory resource

        Returns:
            Response -- JSON serialized list of inventory
        """
        beverage = Beverage.objects.raw(
            '''
            SELECT bev.id, COUNT(trans.beverageId_id) as sold, (bev.quantity - COUNT(trans.beverageId_id)) AS stock FROM
            vendomatic_beverage bev
            LEFT Join vendomatic_transaction trans
            on bev.id = trans.beverageId_id
            GROUP BY trans.beverageId_id;
            '''
        )

        serializer = InventorySerializer(
            beverage,
            many=True,
            context={'request': request}
        )
        return Response({'Array remaining in stock': [beverage[0].stock, beverage[1].stock, beverage[2].stock]}, headers={'X-Coins': beverage[0].stock})

    def update(self, request, pk=None):
        """
        Handles PUT requests for individual transaction
        Returns:
            Response -- Custom Header with total coins and 204 status code
        """
        coin = Coin.objects.all()
        beverage = Beverage.objects.raw(
        '''
        SELECT bev.id as id, bev.quantity as quantity, COUNT(trans.beverageId_id) as sold, (bev.quantity - COUNT(trans.beverageId_id)) AS stock FROM
        vendomatic_beverage bev
        LEFT Join vendomatic_transaction trans
        on bev.id = trans.beverageId_id
        GROUP BY trans.beverageId_id;
            '''
        )
        serializer = InventorySerializer(beverage[int(pk)-1], context={'request': request})
        
        
        for item in coin:
            print(item.coin)
            print(beverage[int(pk)-1].stock <= 0)
            print(beverage[int(pk)-1].stock)
            if item.coin < 2:
                return Response({'X-Coins': item.coin}, status=status.HTTP_404_NOT_FOUND)
            elif beverage[int(pk)-1].stock <= 0:
                return Response({'X-Coins': item.coin}, status=status.HTTP_403_FORBIDDEN)
            else:
                drink = Beverage.objects.get(pk=pk)
                drink.quantity -= 1
                drink.save()
                return Response({'Items Vended': 1}, headers={'X-Coins': item.coin -2, 'X-Inventory-Remaining': beverage[int(pk)-1].stock}, status=status.HTTP_204_NO_CONTENT)
            
            
            

        
        