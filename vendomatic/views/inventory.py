from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vendomatic.models import Beverage, Transaction


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
        fields = ('id', 'beverageType', 'quantity', 'stock')


class Inventories(ViewSet):
    """inventory"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for inventory item

        Returns:
            Response -- JSON serialized inventory instance
        """
        try:
            beverage = Beverage.objects.get(pk=pk)
            serializer = InventorySerializer(beverage, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to inventory resource

        Returns:
            Response -- JSON serialized list of inventory
        """
        beverage = Beverage.objects.raw(
            '''
            SELECT bev.id, bev.quantity, COUNT(trans.beverageId_id) as sold, (bev.quantity - COUNT(trans.beverageId_id)) AS stock FROM
            vendomatic_beverage bev
            LEFT Join vendomatic_transaction trans
            on bev.id = trans.beverageId_id
            GROUP BY trans.beverageId_id;
            '''
        )

        # HttpResponse.__setitem__(header, value)¶
        # Sets the given header name to the given value. Both header and value should be strings.

        # HttpResponse.__getitem__(header)¶
        # Returns the value for the given header name. Case-insensitive.
        

        serializer = InventorySerializer(
            beverage,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)