from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} : {self.department}"


class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number_of_questions = models.IntegerField()
    file = models.FileField(upload_to='exam_files')

    def __str__(self):
        return f"{self.name}"

class ExamResult(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = ArrayField(models.IntegerField())

    def __str__(self):
        return f"{self.user} - {self.exam}"

class ExamBox(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department} - {self.exam}"