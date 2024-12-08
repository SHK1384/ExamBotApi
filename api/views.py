from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import ExamBox, User, ExamResult, Exam

from api.serializers import ExamBoxSerializer, ExamResultSerializer, UserSerializer


# Create your views here.
class ProfileView(ViewSet):

    exam_box_serializer = ExamBoxSerializer
    exam_result_serializer = ExamResultSerializer
    user_serializer = UserSerializer

    def get_exam_box_list(self, request, user_id):
        user = User.objects.get(userid=user_id)
        exam_box = ExamBox.objects.filter(department=user.department)
        serialized_output = self.exam_box_serializer(exam_box, many=True)
        return Response(serialized_output.data, status=status.HTTP_200_OK)

    def add_exam_result(self, request):
        serialized_output = self.exam_result_serializer(data=request.data)
        if serialized_output.is_valid():
            data = serialized_output.data
            user = User.objects.get(userid=data["user_id"])
            exam = Exam.objects.get(id=data["exam_id"])
            exam_result = ExamResult.objects.create(user=user, exam=exam, correct_answer=data["correct_answer"], wrong_answer=data["wrong_answer"], not_answered=data["not_answered"])
            exam_result.save()
            return Response({"message": "Done!"}, status=status.HTTP_200_OK)

    def get_user_by_id(self, request, user_id):
        user = User.objects.get(userid=user_id)
        serialized_output = self.user_serializer(user)
        return Response(serialized_output.data, status=status.HTTP_200_OK)

    def get_prev_exam_result(self, request, user_id, exam_id):
        user = User.objects.get(userid=user_id)
        exam = Exam.objects.get(id=exam_id)
        exam_results = ExamResult.objects.filter(user=user, exam=exam)
        if len(exam_results) == 0:
            return Response({"message": "Ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bad"}, status=status.HTTP_200_OK)
