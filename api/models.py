from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField


# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number_of_questions = models.IntegerField()
    file = models.FileField(upload_to='exam_files')
    answers = ArrayField(models.CharField(), null=True)
    olympiad = models.CharField(max_length=50)
    is_short_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    olympiad = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    current_exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    answers_state = models.TextField(default="")
    set_state_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} : {self.department}"

class ExamResult(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = ArrayField(models.CharField(), null=True)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    correct_answer = models.IntegerField()
    wrong_answer = models.IntegerField()
    not_answered = models.IntegerField()

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