# Kickstarting Fig and Docker - develop and deploy

In this tutorial we'll detailed how to build a powerful development enivornment using Docker, Vagrant, and Fig. We'll also outline a development working that culminates in creating a build and deploying.

> This tutorial is utilizes Docker 1.1.2, Python 2.7.8, Django 1.6.6, all on a Mac OSX machine

## Docker Explained

"[Docker](https://www.docker.com/whatisdocker/) is an open-source engine that automates the deployment of any application as a lightweight, portable, self-sufficient container that will run virtually anywhere."

Docker provides the isolation of a virtual machine, wrapping the filesystem, processes, evironment variables, etc. into a nice container - but without all the overhead since it uses the host machine's kernal. Your app, processes, and code run in *containers*, while *images* save the state of the containers for easy recreation on other machines. Using the popular .git analagy, images are akin to repositores while containers are akin to a local clone.

**Why use Docker?**

1. Containers are isolated like a true VM. Forget about messing with virtualenv.
1. Docker images are shareable and handle version control at the system-level. Easily distrubute your working environment amongst your enture team.

Let's face it: You never really know how your app will perform in production no matter how many times you've tested it out locally because the two environments vary so much. With Docker, you can *truly* mimic your production environment at the local level, with little perfromance loss (since, again, Docker uses the host's Kernel) - which is the "holy grail".

**You can add Docker into your development workflow to test your deployments locally in an isolated, lightweight VM-like environment, all without touching virtualenv.** Pretty cool.

## Fig Explained

[Fig](http://www.fig.sh/) automates the (re)creation of Docker environment.

## Install

1. Follow the instructions [here](http://www.fig.sh/install.html) to install Docker and Fig via [docker-osx](https://github.com/noplay/docker-osx).

1. Sanity check

    Fire up virtualbox and Vagrant:

    ```
    $ docker-osx shell
    $ fig --version
    fig 0.5.2
    ```

> Run `docker-osx` to view the available commands.

## Development Environment - setup

To setup your development environment, you need three files:

### Dockerfile

A Docker file is a configuration file that automates the creation of your container from an image.

```
# start with a base image
FROM ubuntu:13.10

# install dependencies
RUN apt-get -qq update
RUN apt-get install -y python python-pip libmysqlclient-dev python-dev git

# install django dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# expose port 8000 for us to use
EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
```

### fig.yml

A configuration file used to create and manage various Docker images.

```
web:
  build: .
  command: python manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/code
  ports:
    - "8000:8000"
```

This defines one service, `web`, which:

1. Is built from the Docker file in the *current* directory
1. `python manage.py runserver 0.0.0.0:8000` is ran inside the container, which is accessible on port `8000` on the host machine.

### *requirements.txt*

```
Django==1.6.6
```

## Development Environment - creation

### Fire up Vagrant

```
$ docker-osx shell
```

### Create a new Django Project:

```
$ fig run web django-admin.py startproject fig_project .
```

> Talk about cache

### Fire up your app:

```
$ fig up -d
```

> The `up` command sets up and starts the container(s), while the `-d` flag daemonizes the process, leaving it running in the background

Navigate to [http://localdocker:8000/](http://localdocker:8000/) to see it in action. **Yes, you're reading that correctly: It's *localdocker*.**

Then when you're done, just run:

```
$ fig stop
```

## Build your App

Build something. Or say, "Hello, World!" using my app on the repo.

Then test it again. If you need to run `syncdb`, use these commands:

```
$ fig up -d
$ fig run web python manage.py syncdb
```

How about tests?

```
$ fig up -d
$ fig run web python manage.py test
```

Add a few tests if you haven't already.

## Deploy

Right now, there's only a handful of deployment options available for Docker, where you can "push" a Docker image up to it and the service ([IaaS](http://en.wikipedia.org/wiki/Cloud_computing#Infrastructure_as_a_service_.28IaaS.29)) will then create the container based on the config from the image. [Tutum](http://tutum.co) looks to be the most promising, but it's still not production-ready, as of writing. Regardless, I encourage you to check it out, since this process of pushing images will be the future of Docker deployment. The process is simple. Go ahead and sign up.

> If you get stuck, comment below. Or, contact [Tutum](http://tutum.co) directly. They have **excellent** customer support.

Now you can push your local image up to Tutum.

### Find the local image

```
$ docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
deployment_web          latest              e892302872cc        12 hours ago        428.6 MB
```

So, `deployment_web` is the name of the image.

### Push the local image to Tutum's private

```
$ docker login r.tutum.co
$ docker tag <your_local_image_name> r.tutum.co/<tutum_username>/<image_name>
$ docker push r.tutum.co/<tutum_username>/<image_name>
```









....


## Resources

1. Docker Hub (github for docker) images
1. Learn the commands - https://www.docker.com/tryit/
1. https://github.com/wsargent/docker-cheat-sheet
1. http://steveltn.me/blog/2014/03/15/deploy-rails-applications-using-docker/
1. https://speakerdeck.com/clsung/using-fabric-and-docker-for-deployment-testing