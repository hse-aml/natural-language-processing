# Docker container with course dependencies

This file describes how to use a Docker container with Jupyter notebook and
all dependencies required for the course.

The image is located at https://hub.docker.com/r/akashin/coursera-aml-nlp/.

## Install Stable Docker Community Edition (CE)

- For Mac: 
https://docs.docker.com/docker-for-mac/install/

- For Ubuntu: 
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/ (see also other Linux distributives in the menu).

- For Windows (64bit Windows 10 Pro, Enterprise and Education):
https://docs.docker.com/docker-for-windows/install/ 

- For Windows (older versions):
https://docs.docker.com/toolbox/toolbox_install_windows/



## Get container image

To get the latest version of the container image run:
```sh
docker pull akashin/coursera-aml-nlp
```
It containes Ubuntu 16.04 Linux distirbutive and all dependencies that you need for our course. The downloaded image takes approximately 2.3GB. 

**Note:** If you are getting an error "Got permission denied while trying to connect to the Docker daemon socket...", you need to add current user to the docker group:
```sh
sudo usermod -a -G docker $USER
sudo service docker restart
```
Then you need to logout and login to the system again (disconnect and connect to your AWS instance if you are setting up a docker on it).


## Run container for the first time

Now you can start new container from this image with:
```sh
docker run -it -p 127.0.0.1:8080:8080 --name coursera-aml-nlp akashin/coursera-aml-nlp
```
This will start the Ubuntu instance and give you an access to its command line. You can type `run_notebook` to launch IPython notebook server. 

You may find it useful to mount a directory from your local machine within the container using `-v` option:
```sh
docker run -it -p 127.0.0.1:8080:8080 --name coursera-aml-nlp -v $PWD:/root/coursera akashin/coursera-aml-nlp
```
This will use shell alias `$PWD` to mount current directory to the folder `/root/coursera` in the container. Alternatively, you can mount arbitrary directory by replacing `$PWD` with a custom path.

## Stop and resume container

To stop the container use:
```sh
docker stop coursera-aml-nlp
```
All the changes that were made within container will be saved.

To resume the stopped container use:
```sh
docker start -i coursera-aml-nlp
```
## Other operations on the container

There are many other operations that you can perform on the container, to show all of them:
```sh
docker container
```
Some particularly useful would be **showing a list of containers** and **removing container**.

To show currently running and stopped containers with their status:
```sh
docker ps -a
```

To remove the container and all data associated with it:
```sh
docker rm coursera-aml-nlp
```
Note, that this will remove all the internal data of the container (e.g. installed packages), but all the data written inside of your local mounted folder (`-v` option) will not be affected.

## Install more packages

You can install more packages in the container if needed:
```sh
docker exec coursera-aml-nlp pip3 install PACKAGE_NAME
```

## Change RAM limits of the container

Your container might have memory limits that are different from the actual limits of your physical machine, which might lead to a crash of your code due memory shortage.

* If you're running Windows or OSX, the default limit is 2GB, but you can change it by following this tutorials:
  * For Windows: https://docs.docker.com/docker-for-windows/#advanced
  * For Mac OSX: https://docs.docker.com/docker-for-mac/#advanced

* If you're running Linux, you're all set as the memory limits are the same as the physical memory of your machine.


## Further reading

If you are interested to know more about Docker, check out this articles: 
- Using Jupyter notebook from Docker: https://www.dataquest.io/blog/docker-data-science/
- General introduction to Docker: https://docker-curriculum.com/


## Credits

The template for this dockerfile was taken from https://github.com/ZEMUSHKA/coursera-aml-docker
