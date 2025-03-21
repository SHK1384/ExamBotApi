from operator import index
from warnings import catch_warnings

from django.shortcuts import render
from django.views.decorators.cache import never_cache, cache_control

from api.models import Department, User
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
        cnt = 0
        for image in image_file:
            image_bytes = image.read()
            try:
                resp = process_image(image_bytes)
            except Exception as e:
                print(e)
                lists.append("عکس نامطلوب")
                continue

            if resp == "Bad":
                lists.append("عکس نامطلوب")
                continue
            wrong = 0
            correct = 0
            not_answer = 0
            for i in range(len(key)):
                if resp[i].count(1) > 1:
                    lists.append("عکس نامطلوب")
                    continue
                if resp[i].count(1) == 0:
                    not_answer += 1
                elif resp[i].index(1) == int(key[i])-1:
                    correct += 1
                else:
                    wrong += 1
            percent = ((correct*4-wrong)*100)/(len(key)*4)
            lists.append(round(percent, 2))
            student = User.objects.get(id=int(request.POST.get(f'object_{cnt}')))
            students.append(student.first_name + ' ' + student.last_name)
            cnt += 1
        print(lists)
        print(students)
        return render(request, 'optical/examined.html', {'sp': zip(students, lists)})
    elif request.method == 'POST':
        departments = Department.objects.all()
        students = User.objects.all().exclude(department__id=11)
        return render(request, 'optical/index.html', {'error': True, 'departments': departments, 'students': students})
    departments = Department.objects.all()
    students = User.objects.all().exclude(department__id=11)
    return render(request, 'optical/index.html', context={'departments': departments, 'students': students})
