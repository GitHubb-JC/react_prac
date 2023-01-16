from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import ReviewSerializer
from .models import Review

# Create your views here.
class ReviewList(APIView): # 목록 보여주는
    def get(self, request): # 리스트 보여줄 때
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True) # 여러 객체 serializer 하려면 many=True 해야해
        return Response(serializer.data)

    def post(self, request): # 새 글 작성시
        serializer = ReviewSerializer(data=request.data) # request.data 는 사용자 입력 데이터
        if serializer.is_valid(): # 유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    def get_object(self, pk): # review 객체 가져오기
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None): # review detail 보기
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk, format=None): # review 수정하기
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(): # 유효성 검사
            serializer.save() # 저장
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None): # review 삭제하기
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)