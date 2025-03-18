from operator import index

from django.shortcuts import render

from .script import process_image

def processing(request):
    if request.method == 'POST' and request.FILES.get('image') and request.POST.get('key'):
        image_file = request.FILES['image']
        key = str(request.POST['key']).split(',')
        image_bytes = image_file.read()
        resp = process_image(image_bytes)
        if resp == "please reCapture the picture please":
            print("wtf")
            return render(request, 'optical/index.html', {'error': "recapture"})
        wrong = 0
        correct = 0
        not_answer = 0
        for i in range(len(key)):
            if resp[i].count(1) > 1:
                return render(request, 'optical/index.html', {'error': "recapture"})
            if resp[i].count(1) == 0:
                not_answer += 1
            elif resp[i].index(1) == int(key[i])-1:
                correct += 1
            else:
                wrong += 1
        percent = ((correct*4-wrong)*100)/(len(key)*4)
        return render(request, 'optical/examined.html', {'wrong': wrong, 'correct': correct, 'not_answer': not_answer, 'percent': percent})
    else:
        return render(request, 'optical/index.html')
