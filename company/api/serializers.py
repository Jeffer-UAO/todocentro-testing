from rest_framework.serializers import ModelSerializer
from company.models import Company


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = ['id_n', 'email', 'company', 'web', 'we',
                  'address', 'phone', 'whatsaap', 'updated_at', 'created_at']
