from django.template.backends.django import reraise
from rest_framework import serializers

from api.models import ExamBox, Exam, Department, User

class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    userid = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    olympiad = serializers.CharField(required=False)

    def validate_olympiad(self, value):
        if value != 'Math' and value !='Chem' and value != 'Info':
            raise serializers.ValidationError("Olympiad not found!")
        return value

class ExamResultSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.CharField())
    start_time = serializers.DateTimeField()
    finish_time = serializers.DateTimeField()
    correct_answer = serializers.IntegerField()
    wrong_answer = serializers.IntegerField()
    not_answered = serializers.IntegerField()

class ExamSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(child=serializers.CharField(), required=False)
    class Meta:
        model = Exam
        fields = '__all__'

class UserStateSetSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    state = serializers.CharField()
    current_exam = serializers.IntegerField()
    set_state_time = serializers.DateTimeField(required=False)

class UserStateGetSerializer(serializers.Serializer):
    state = serializers.CharField()
    current_exam = ExamSerializer()
    set_state_time = serializers.DateTimeField()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ExamBoxSerializer(serializers.ModelSerializer):
    exam = ExamSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = ExamBox
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    current_exam = ExamSerializer()

    class Meta:
        model = User
        fields = '__all__'

class SetUserAnswerState(serializers.Serializer):
    user_id = serializers.CharField()
    answers_state = serializers.CharField()

class SetUserCurrentMessageId(serializers.Serializer):
    user_id = serializers.CharField()
    current_message_id = serializers.CharField()

class SetCurrentQuestion(serializers.Serializer):
    user_id = serializers.CharField()
    current_question = serializers.CharField()

class SetCurrentExamMessageId(serializers.Serializer):
    user_id = serializers.CharField()
    current_message_id = serializers.CharField()

class SetCurrentPage(serializers.Serializer):
    user_id = serializers.CharField()
    current_page = serializers.IntegerField()

class SetCurrentVipMessageId(serializers.Serializer):
    user_id = serializers.CharField()
    current_vip_message_id = serializers.CharField()
