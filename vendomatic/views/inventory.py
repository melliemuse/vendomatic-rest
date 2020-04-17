from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vendomatic.models import Beverage, Coin, Transaction


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for inventory

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
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


        transaction = Transaction.objects.all()
        coin = Coin.objects.all()
        coin = self.request.query_params.get('coin', None)
        beverage = Beverage.objects.all()
        beverage = self.request.query_params.get('id', None)

        # if match is not None:
        #     message = message.filter(match__id=match)

        if coin.coin > 2:

            
            

            return Response({'X-Coins': coin.coin}, status=status.HTTP_404_NOT_FOUND)
        
            # return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    

        return Response({'Items Vended': beverage[0].sold}, headers={'X-Coins': coin.coin -2, 'X-Inventory-Remaining': beverage[0].stock}, status=status.HTTP_204_NO_CONTENT)
        # return Response(headers={'X-coins': coin.coin}, status=status.HTTP_204_NO_CONTENT)