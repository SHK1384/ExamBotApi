from rest_framework import serializers

from api.models import ExamBox, Exam, Department, User


class ExamResultSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    correct_answer = serializers.IntegerField()
    wrong_answer = serializers.IntegerField()
    not_answered = serializers.IntegerField()

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class UserStateSetSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    state = serializers.CharField()
    current_exam = serializers.IntegerField()

class UserStateGetSerializer(serializers.Serializer):
    state = serializers.CharField()
    current_exam = ExamSerializer()

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

    class Meta:
        model = User
        fields = '__all__'
