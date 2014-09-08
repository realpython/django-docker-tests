# start with a base image
FROM ubuntu:13.10
MAINTAINER Real Python <info@realpython.com>

# install dependencies
RUN apt-get update
RUN apt-get install -y python python-pip libmysqlclient-dev python-dev

# grab contents of source directory
ADD ./src /src/

# specify working directory
WORKDIR /src

# build app
RUN pip install -r requirements.txt
RUN python manage.py syncdb --noinput

# expose port 8000 for us to use
EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000