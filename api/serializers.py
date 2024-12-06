from rest_framework import serializers

from api.models import ExamBox, Exam, Department

class ExamResultSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.IntegerField())

class ExamBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamBox
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
