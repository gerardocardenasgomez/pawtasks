FROM python:2.7.15-slim-stretch
ARG token

RUN apt-get install git -y
RUN git config --global url.”https://${token}:@github.com/".insteadOf “https://github.com/"

RUN git clone -b 'v1.0' --single-branch  --depth 1 https://github.com/gerardocardenasgomez/pawtasks.git
