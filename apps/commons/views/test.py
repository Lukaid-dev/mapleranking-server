from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema


class Test(APIView):
    """
    # api test용
    - 단순 테스트용입니다. 신경쓰지 마세요.
    """

    @swagger_auto_schema(
        operation_description="""
        # For Test
        """,
        # responses={
        #     200: PostGetSerializer(many=True),
        # },
    )
    def get(self, request):
        # random_generated_to_post()
        # tmp = PostGenerated.objects.filter(
        #     updated_at__gte=datetime.datetime.now() - datetime.timedelta(days=1),
        # ).all()
        # print(len(tmp))

        # user = request.user

        # posts = user.posts.all()

        # print(len(posts))

        return Response(status=status.HTTP_200_OK)
