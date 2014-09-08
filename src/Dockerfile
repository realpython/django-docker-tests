FROM ubuntu:13.10
RUN apt-get -qq update
RUN apt-get install -y python python-pip libmysqlclient-dev python-dev
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000