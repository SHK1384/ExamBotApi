from rest_framework import serializers

from api.models import ExamBox, Exam, Department, User


class ExamResultSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.IntegerField())

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

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
