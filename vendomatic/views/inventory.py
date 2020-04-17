from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vendomatic.models import Beverage


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
            return Response(serializer.data, headers={'Remaining Item Quantity': beverage[int(pk)-1].stock})
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
        return Response(serializer.data, headers={'X-Coins': beverage[0].stock})