from operator import index
from warnings import catch_warnings

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache, cache_control
from rest_framework.status import HTTP_404_NOT_FOUND

from api.models import Department, User, FileBox, Exam
from .script import process_image

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def processing(request):
    if request.method == 'POST' and request.FILES.getlist('images') and request.POST.get('key') and request.POST.get('count'):
        image_file = request.FILES.getlist('images')
        questions_count = request.POST.get('count')
        try:
            questions_count = int(questions_count)
        except ValueError:
            departments = Department.objects.all()
            students = User.objects.all().exclude(department__id=11)
            return render(request, 'optical/index.html', context={'departments': departments, 'students': students})


        key = str(request.POST['key']).split(',')
        if len(key) != questions_count:
            departments = Department.objects.all()
            students = User.objects.all().exclude(department__id=11)
            return render(request, 'optical/index.html', context={'departments': departments, 'students': students})
        lists = []
        students = []
        wrongs = []
        corrects = []
        not_answereds = []
        cnt = 0
        for image in image_file:
            image_bytes = image.read()
            try:
                resp = process_image(image_bytes)
            except Exception as e:
                print(e)
                lists.append("عکس نامطلوب")
                corrects.append(0)
                wrongs.append(0)
                not_answereds.append(0)
                student = User.objects.get(id=int(request.POST.get(f'object_{cnt}')))
                students.append(student.first_name + ' ' + student.last_name)
                cnt += 1
                continue

            if resp == "Bad":
                lists.append("عکس نامطلوب")
                corrects.append(0)
                wrongs.append(0)
                not_answereds.append(0)
                student = User.objects.get(id=int(request.POST.get(f'object_{cnt}')))
                students.append(student.first_name + ' ' + student.last_name)
                cnt += 1
                continue
            wrong = 0
            correct = 0
            not_answer = 0
            image_falty = False
            for i in range(len(key)):
                if resp[i].count(1) > 1:
                    lists.append("عکس نامطلوب")
                    image_falty = True
                    break
                if resp[i].count(1) == 0:
                    not_answer += 1
                elif resp[i].index(1) == int(key[i])-1:
                    correct += 1
                else:
                    wrong += 1
            if not image_falty:
                corrects.append(correct)
                wrongs.append(wrong)
                not_answereds.append(not_answer)
                percent = ((correct*4-wrong)*100)/(len(key)*4)
                lists.append(round(percent, 2))
            else:
                corrects.append(0)
                wrongs.append(0)
                not_answereds.append(0)
            student = User.objects.get(id=int(request.POST.get(f'object_{cnt}')))
            students.append(student.first_name + ' ' + student.last_name)
            cnt += 1
        return render(request, 'optical/examined.html', {'sp': zip(students, lists, corrects, wrongs, not_answereds)})
    elif request.method == 'POST':
        departments = Department.objects.all()
        students = User.objects.all().exclude(department__id=11)
        return render(request, 'optical/index.html', {'error': True, 'departments': departments, 'students': students})
    departments = Department.objects.all()
    students = User.objects.all().exclude(department__id=11)
    return render(request, 'optical/index.html', context={'departments': departments, 'students': students})

def success(request):
    return render(request, 'optical/success.html')

def add_tashrihi(request, userid):
    if not User.objects.filter(userid=userid).exists():
        return HttpResponse(HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        with transaction.atomic():
            print("POST")
            user = User.objects.get(userid=userid)
            file1 = request.FILES.get('file1')
            file2 = request.FILES.get('file2')
            file3 = request.FILES.get('file3')
            file4 = request.FILES.get('file4')

            exam = Exam.objects.get(id=46)
            if not FileBox.objects.filter(user=user, question=1).exists():
                filebox1 = FileBox(user=user, exam=exam, question=1, file=file1)
                filebox1.save()
            else:
                filebox1 = FileBox.objects.get(user=user, question=1)
                filebox1.file = file1
                filebox1.save()

            if not FileBox.objects.filter(user=user, question=2).exists():
                filebox2 = FileBox(user=user, exam=exam, question=2, file=file2)
                filebox2.save()
            else:
                filebox2 = FileBox.objects.get(user=user, question=2)
                filebox2.file = file2
                filebox2.save()

            if not FileBox.objects.filter(user=user, question=3).exists():
                filebox3 = FileBox(user=user, exam=exam, question=3, file=file3)
                filebox3.save()
            else:
                filebox3 = FileBox.objects.get(user=user, question=3)
                filebox3.file = file3
                filebox3.save()


            if not FileBox.objects.filter(user=user, question=4).exists():
                filebox4 = FileBox(user=user, exam=exam, question=4, file=file4)
                filebox4.save()
            else:
                filebox4 = FileBox.objects.get(user=user, question=4)
                filebox4.file = file3
                filebox4.save()

        return render(request, 'optical/success.html')
    return render(request, 'optical/tashrihi.html')