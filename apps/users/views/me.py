from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

from apps.users.models import User
from apps.users.serializers.me import MeSerializer


class Me(APIView):
    @swagger_auto_schema(
        operation_description="내 정보를 가져옵니다.",
        responses={
            200: MeSerializer(),
        },
    )
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = MeSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
