from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from jjim.models import Jjim
from jjim.serializers import JjimSerializer


class JjimAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        book_id = request.data.get("book_id")

        # 사용자와 도서가 존재하는지 확인
        jjim = Jjim.objects.filter(user_id=user_id, book_id=book_id).first()  # 중복을 방지하기 위해 filter() 사용

        if jjim:
            jjim.quantity += 1
            jjim.save()
        else:
            jjim = Jjim.objects.create(
                user_id=user_id,
                book_id=book_id,
                quantity=1
            )

        # 직렬화 및 응답
        serializer = JjimSerializer(jjim)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
