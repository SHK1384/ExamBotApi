from datetime import datetime
from http.client import responses
from types import NoneType

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import ExamBox, User, ExamResult, Exam, Department

from api.serializers import ExamBoxSerializer, ExamResultSerializer, UserSerializer, UserStateGetSerializer, \
    UserStateSetSerializer, UserRegisterSerializer


# Create your views here.
# testing something

def exam_id(request):
    exams = Exam.objects.all()
    result = ""
    for exam in exams:
        result += exam.id + ": " + exam.name + "\n"
    return HttpResponse(result)


def result_view(request, department_id, exam_id):
    exam_results = ExamResult.objects.filter(exam__id=exam_id, user__department__id=department_id)
    result = Exam.objects.get(id=exam_id).name + "\n"
    exam_answer_sheet = Exam.objects.get(id=exam_id).answers
    for exam_result in exam_results:
        user_answer_sheet = exam_result.answers
        correct = 0
        not_answered = 0
        wrong = 0
        for i in range(len(user_answer_sheet)):
            if user_answer_sheet[i] == exam_answer_sheet[i]:
                correct += 1
            elif 1 <= user_answer_sheet[i] <= 5:
                wrong += 1
            else:
                not_answered += 1
        exam_result.correct_answer = correct
        exam_result.wrong_answer = wrong
        exam_result.not_answered = not_answered
        exam_result.save()
        result += exam_result.user.first_name + " " + exam_result.user.last_name + ": " + str(25*(exam_result.correct_answer*4-exam_result.wrong_answer)/(exam_result.correct_answer+exam_result.wrong_answer+exam_result.not_answered)) + "\n"
        #important comments
    return HttpResponse(result)

class ProfileView(ViewSet):

    exam_box_serializer = ExamBoxSerializer
    exam_result_serializer = ExamResultSerializer
    user_serializer = UserSerializer
    user_state_get_serializer = UserStateGetSerializer
    user_state_set_serializer = UserStateSetSerializer
    user_register_serializer = UserRegisterSerializer

    def register_new_user(self, request):
        serializer_output = self.user_register_serializer(data=request.data)
        if serializer_output.is_valid(raise_exception=True):
            department = Department.objects.get(id=11)
            new_user = User.objects.create(first_name=request.data['first_name'], last_name=request.data['last_name'], userid=request.data['userid'], department=department, state="None", set_state_time=datetime.now())
            new_user.save()
            return Response({"message": "Done!"}, status=status.HTTP_200_OK)

    def get_exam_box_list(self, request, user_id):
        user = User.objects.get(userid=user_id)
        exam_box = ExamBox.objects.filter(department=user.department)
        serialized_output = self.exam_box_serializer(exam_box, many=True)
        return Response(serialized_output.data, status=status.HTTP_200_OK)

    def add_exam_result(self, request):
        serialized_output = self.exam_result_serializer(data=request.data)
        if serialized_output.is_valid(raise_exception=True):
            data = serialized_output.data
            user = User.objects.get(userid=data["user_id"])
            exam = Exam.objects.get(id=data["exam_id"])
            exam_result = ExamResult.objects.create(user=user, exam=exam, answers=data["answers"], answers_short_answer=data['answers_short_answer'], start_time=data["start_time"], finish_time=data["finish_time"], correct_answer=data["correct_answer"], wrong_answer=data["wrong_answer"], not_answered=data["not_answered"])
            exam_result.save()
            return Response({"message": "Done!"}, status=status.HTTP_200_OK)

    def get_user_by_id(self, request, user_id):
        if not User.objects.filter(userid=user_id).exists():
            return Response({"message": "not found"}, status=status.HTTP_200_OK)
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

    def get_user_state(self, request, user_id):
        user = User.objects.get(userid=user_id)
        if user.state == "None" or user.state == "" or user.current_exam is None:
            return Response({"state": "None"}, status=status.HTTP_200_OK)
        data = {'set_state_time': user.set_state_time ,'state': user.state, 'current_exam': user.current_exam}
        serialized_output = self.user_state_get_serializer(data)
        return Response(serialized_output.data, status=status.HTTP_200_OK)

    def set_user_state(self, request):
        serialized_output = self.user_state_set_serializer(data=request.data)
        if serialized_output.is_valid(raise_exception=True):
            user = User.objects.get(userid=serialized_output.data['user_id'])
            if serialized_output.data['current_exam'] == -1:
                user.state = "None"
                user.current_exam = None
                user.save()
            else:
                exam = Exam.objects.get(id=serialized_output.data['current_exam'])
                user.state = serialized_output.data['state']
                user.current_exam = exam
                user.set_state_time = serialized_output.data['set_state_time']
                user.save()
            return Response({"message": "Done"}, status=status.HTTP_200_OK)