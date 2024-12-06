FROM hub.hamdocker.ir/library/python:3.13
WORKDIR /ExamBotApi/
ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt
ADD ./ ./
ENTRYPOINT ["/bin/sh", "-c" , "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 ExamBotApi.wsgi"]