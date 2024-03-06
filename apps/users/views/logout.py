from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated

from firebase_admin import auth

from drf_yasg.utils import swagger_auto_schema


from apps.users.models import UserSession


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    """
    프론트에서 firebase auth에 토큰 만료 요청 때리고, 서버에선 세션만 닫아주면 될듯?
    """

    @swagger_auto_schema(
        operation_description="""
        ## 로그아웃 시 요청하는 api
        - firebase auth logout과 별개로 로그아웃 할때 요청해주세요
        - 사용자의 리프레시 토큰은 만료됩니다.
        """,
        responses={
            200: "HTTP_200_OK",
        },
    )
    def put(self, request):
        # 토큰 만료
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        id_token = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get("uid")
        auth.revoke_refresh_tokens(uid)

        sessions = UserSession.objects.filter(
            user=request.user, logged_out_at__isnull=True
        )
        session = sessions.last()
        session.logged_out_at = timezone.now()
        session.is_expired = True
        session.save()

        return Response(status=HTTP_200_OK)
