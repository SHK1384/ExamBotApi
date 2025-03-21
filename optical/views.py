from operator import index

from django.shortcuts import render

from api.models import Department, User
from .script import process_image

def processing(request):
    if request.method == 'POST' and request.FILES.getlist('images') and request.POST.get('key'):
        image_file = request.FILES.getlist('images')
        key = str(request.POST['key']).split(',')
        lists = []
        students = []
        cnt = 0
        for image in image_file:
            image_bytes = image.read()
            resp = process_image(image_bytes)
            if resp == "Bad":
                print("wtf")
                return render(request, 'optical/index.html', {'error': "recapture"})
            wrong = 0
            correct = 0
            not_answer = 0
            for i in range(len(key)):
                if resp[i].count(1) > 1:
                    print("suuuuupppp")
                    return render(request, 'optical/index.html', {'error': "recapture"})
                if resp[i].count(1) == 0:
                    not_answer += 1
                elif resp[i].index(1) == int(key[i])-1:
                    correct += 1
                else:
                    wrong += 1
            percent = ((correct*4-wrong)*100)/(len(key)*4)
            lists.append(percent)
            student = User.objects.get(id=int(request.POST.get(f'object_{cnt}')))
            students.append(student.first_name + student.last_name)
            cnt += 1
        print(lists)
        print(students)
        return render(request, 'optical/examined.html', {'sp': zip(students, lists)})
    else:
        departments = Department.objects.all()
        students = User.objects.all().exclude(department__id=11)
        return render(request, 'optical/index.html', context={'departments': departments, 'students': students})
