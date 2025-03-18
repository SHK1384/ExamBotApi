FROM hub.hamdocker.ir/library/python:3.13
WORKDIR /ExamBotApi/
ADD ./requirements.txt ./
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install -r ./requirements.txt
ADD ./ ./
ENTRYPOINT ["/bin/sh", "-c" , "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 ExamBotApi.wsgi"]