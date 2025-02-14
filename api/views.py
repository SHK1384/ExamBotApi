from datetime import datetime
from http.client import responses
from itertools import permutations
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
    exams=Exam.objects.all()
    for exam in exams:
        if exam.is_short_answer:
            exam.answers = exam.answers_short_answer
        else:
            exam.answers_short_answer = exam.answers
        exam.save()
    return Response({"message": "Done"}, status=status.HTTP_200_OK)
    # if department_id != 11:
    #     exam_results = ExamResult.objects.filter(exam__id=exam_id, user__department__id=department_id)
    # else:
    #     exam_results = ExamResult.objects.filter(exam__id=exam_id)
    # result = Exam.objects.get(id=exam_id).name + "\n"
    # exam_answer_sheet = Exam.objects.get(id=exam_id).answers
    #
    # correct_questions = [0] * Exam.objects.get(id=exam_id).number_of_questions
    # wrong_questions = [0] * Exam.objects.get(id=exam_id).number_of_questions
    # not_answered_questions = [0] * Exam.objects.get(id=exam_id).number_of_questions
    #
    # precent_raw = ""
    # for exam_result in exam_results:
    #     user_answer_sheet = exam_result.answers
    #     correct = 0
    #     not_answered = 0
    #     wrong = 0
    #     for i in range(len(user_answer_sheet)):
    #         if user_answer_sheet[i] == exam_answer_sheet[i]:
    #             correct += 1
    #             correct_questions[i] += 1
    #         elif 1 <= user_answer_sheet[i] <= 5:
    #             wrong += 1
    #             wrong_questions[i] += 1
    #         else:
    #             not_answered += 1
    #             not_answered_questions[i] += 1
    #
    #     exam_result.correct_answer = correct
    #     exam_result.wrong_answer = wrong
    #     exam_result.not_answered = not_answered
    #     exam_result.save()
    #     precent_raw += str(25*(exam_result.correct_answer*4-exam_result.wrong_answer)/(exam_result.correct_answer+exam_result.wrong_answer+exam_result.not_answered))
    #     result += exam_result.user.first_name + " " + exam_result.user.last_name + ": " + str(25*(exam_result.correct_answer*4-exam_result.wrong_answer)/(exam_result.correct_answer+exam_result.wrong_answer+exam_result.not_answered)) + "\n"
    #
    # result += '\n\n\n'
    # result += 'index correct wrong empty\n'
    # for i in range(len(correct_questions)):
    #     result += str(i + 1) + " " + str(correct_questions[i]) + " " + str(wrong_questions[i]) + " " + str(
    #         not_answered_questions[i]) + "\n"
    # result += '\n\n\n'
    # result += precent_raw
    # return HttpResponse(result)

class ProfileView(ViewSet):

    exam_box_serializer = ExamBoxSerializer
    exam_result_serializer = ExamResultSerializer
    user_serializer = UserSerializer
    user_state_get_serializer = UserStateGetSerializer
    user_state_set_serializer = UserStateSetSerializer
    user_register_serializer = UserRegisterSerializer

    def get_all_users(self, request):
        users = User.objects.all()
        serializer_output = self.user_serializer(users, many=True)
        return Response(serializer_output.data, status=status.HTTP_200_OK)

    def update_new_user(self, request):
        serializer_output = self.user_register_serializer(data=request.data)
        if serializer_output.is_valid(raise_exception=True):
            user = User.objects.get(userid=request.data['userid'])
            data = serializer_output.data
            if data.get("first_name", "none") != "none":
                user.first_name = data["first_name"]
            if data.get("last_name", "none") != "none":
                user.last_name = data["last_name"]
            if data.get("olympiad", "none") != "none":
                user.olympiad = data["olympiad"]
            if data.get("state", "none") != "none":
                user.state = data["state"]
                user.set_state_time = datetime.now()
            user.save()
            return Response({"message": "Done!"}, status=status.HTTP_200_OK)

    def register_new_user(self, request):
        serializer_output = self.user_register_serializer(data=request.data)
        if serializer_output.is_valid(raise_exception=True):
            department = Department.objects.get(id=11)
            data = serializer_output.data
            new_user = User.objects.create(first_name="", last_name="", userid=data['userid'], department=department, state=data['state'], set_state_time=datetime.now())
            new_user.save()
            return Response({"message": "Done!"}, status=status.HTTP_200_OK)

    def get_exam_box_list(self, request, user_id):
        user = User.objects.get(userid=user_id)
        if user.olympiad == "Math" or user.olympiad == "Info":
            exam_box = (ExamBox.objects.filter(department=user.department, exam__olympiad="Math") |
                        ExamBox.objects.filter(department=user.department, exam__olympiad="Info"))
        else:
            exam_box = ExamBox.objects.filter(department=user.department, exam__olympiad=user.olympiad)
        serialized_output = self.exam_box_serializer(exam_box, many=True)
        return Response(serialized_output.data, status=status.HTTP_200_OK)

    def add_exam_result(self, request):
        serialized_output = self.exam_result_serializer(data=request.data)
        if serialized_output.is_valid(raise_exception=True):
            data = serialized_output.data
            user = User.objects.get(userid=data["user_id"])
            exam = Exam.objects.get(id=data["exam_id"])
            exam_result = ExamResult.objects.create(user=user, exam=exam, answers=data["answers"], start_time=data["start_time"], finish_time=data["finish_time"], correct_answer=data["correct_answer"], wrong_answer=data["wrong_answer"], not_answered=data["not_answered"])
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