FROM python:2.7.15-slim-stretch
ADD ./* /root/
WORKDIR "/root"
RUN apt-get update -y && apt-get install libpq-dev gcc -y
RUN pip install -r /root/requirements.txt
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app" ]
