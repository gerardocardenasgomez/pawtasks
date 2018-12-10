FROM postgres:9.6-alpine
ADD ./* /root/
WORKDIR "/root/"
RUN apk add --update gcc py-pip musl-dev python-dev
RUN pip install -r requirements.txt
