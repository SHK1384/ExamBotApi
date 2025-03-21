from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField, ForeignKey


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
    is_long_answer = models.BooleanField(default=False)

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
    current_question = models.CharField(max_length=100, default="")
    current_message_id = models.CharField(max_length=500, default="")
    current_exam_message_id = models.CharField(max_length=500, default="")
    current_page = models.IntegerField(default=0)
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


class FileBox(models.Model):
    id = models.AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.CharField(max_length=50)
    advice = models.TextField(default="")
    score = models.IntegerField(default=0)
    file = models.FileField(upload_to='user_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} : {self.exam} - {self.question}"

class ExamResultLong(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fileboxes = models.ManyToManyField(FileBox)

    def __str__(self):
        return f"{self.user} - {self.exam}"
