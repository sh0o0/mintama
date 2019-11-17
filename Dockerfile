FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /mintama
WORKDIR /mintama
ADD ./Pipfile /mintama/
RUN pip install pipenv
RUN pipenv install
ADD . /mintama/