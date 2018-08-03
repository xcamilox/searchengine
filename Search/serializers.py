from Search.models import Catalog
from rest_framework import serializers


class CatalogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Catalog
        fields = ('id','tables')