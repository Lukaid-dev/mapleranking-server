from rest_framework.serializers import ModelSerializer
from ..models import User


class MeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "email",
        )
