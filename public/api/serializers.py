from rest_framework.serializers import ModelSerializer
from customers.models import Domain


class DomainSerializer(ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "domain"]