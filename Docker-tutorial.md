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

Now you can start new container from this image with the following command:
```sh
docker run -it -p 8080:8080 --name coursera-aml-nlp akashin/coursera-aml-nlp -v path_on_your_machine:path_within_docker
```
This will start the Ubuntu instance and give you an access to its command line. You can type `run_notebook` to launch IPython notebook server.

Note that we are using `-p 8080:8080` argument to set up port forwarding to make IPython notebook accessible at address http://localhost:8080. If you're using AWS, make sure that you've [set up the port forwarding](https://github.com/hse-aml/natural-language-processing/blob/master/AWS-tutorial.md#2-set-up-dependencies-and-run-your-project) there as well.

**Important:** Docker image only contains system dependencies for the project (e.g. TensorFlow, Starspace).
All other project-related files (e.g. input data) need to be exposed to the container manually though [Docker volumes](https://docs.docker.com/storage/volumes/). To do this, we are mounting a directory from your machine within the container using `-v` option.

On Linux and OSX, an example command looks like:
```sh
docker run -it -p 8080:8080 --name coursera-aml-nlp -v $PWD:/root/coursera akashin/coursera-aml-nlp
```
This will use shell alias `$PWD` to mount current directory to the folder `/root/coursera` in the container. Alternatively, you can mount arbitrary directory by replacing `$PWD` with a custom path.

**On Windows**, there are some extra [steps](https://rominirani.com/docker-on-windows-mounting-host-directories-d96f3f056a2c) involved, and the launch command looks like
```sh
docker run -it -p 8080:8080 --name coursera-aml-nlp --user root -v /c/Users/$YOUR_USERNAME:/root/coursera akashin/coursera-aml-nlp
```
Where `/c/Users/$YOUR_USERNAME` is the path to your user's home folder.

If you're using Docker Toolbox on Windows, the command given above might not work because of the additional VirtualBox layer involved. Instead, we recommend that you follow the guidance in http://blog.shahinrostami.com/2017/11/docker-toolbox-windows-7-shared-volumes/.

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

To connect to a Bash shell in the already running container with name `coursera-aml-nlp` run:
```
docker exec -it coursera-aml-nlp bash
```
This will drop you into the standard Linux Bash shell that supports common commands like `ls`, `wget` or `python3`.

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

- If you're running Windows or OSX, the default limit is 2GB, but you can change it by following this tutorials:
  - For Windows: https://docs.docker.com/docker-for-windows/#advanced
  - For Mac OSX: https://docs.docker.com/docker-for-mac/#advanced

- If you're running Linux, you're all set as the memory limits are the same as the physical memory of your machine.


## Further reading

If you are interested to know more about Docker, check out this articles: 
- Using Jupyter notebook from Docker: https://www.dataquest.io/blog/docker-data-science/
- General introduction to Docker: https://docker-curriculum.com/

## Troubleshooting

### Verify your Docker installation by running "Hello World" application
- Run `docker pull hello-world`. You should see a message that ends with 
    “Status: Downloaded newer image for hello-world:latest”.
- Run `docker run hello-world`.  You should see a message that starts with
    “Hello from Docker!
    This message shows that your installation appears to be working correctly.”

If you see any errors, follow relevant troubleshooting steps.

### “Unauthorized: authentication required” when trying to pull Docker image
Run `docker logout` and try pulling again. If this doesn't help, make sure the system date is set correctly and try again. If this doesn't help, reinstall Docker and try again.

### Can't open Jupyter notebook in the browser
If you try to open "http://localhost:8080" or "http://127.0.0.1:8080" in your browser, when `run_notebook` command is started, and you can't access your notebooks, here are some advices:
- If you're using Docker Toolbox on Windows, try accessing "http://192.168.99.100:8080" instead. If this doesn't work, follow the instructions [on official Docker docs](https://docs.docker.com/docker-for-windows/troubleshoot/#limitations-of-windows-containers-for-localhost-and-published-ports) and on [Stackoverflow](https://stackoverflow.com/questions/42866013/docker-toolbox-localhost-not-working).
- Make sure that you're running container with `-p` flag as described [here](#run-container-for-the-first-time) and that the output of `docker ps` contains a message like this:
```
CONTAINER ID        IMAGE                      COMMAND             CREATED                  STATUS              PORTS               NAMES
e5b7bcd85a1b        akashin/coursera-aml-nlp   "/bin/bash"         Less than a second ago   Up 2 seconds        8080/tcp            peaceful_lamarr
```
If the part about `PORTS` differs, remove the current container following [instructions](#other-operations-on-the-container) and start it again.
- Make sure that browser proxy settings don't interfere with accessing local web sites.
- If you're running Docker on AWS, make sure you've set up port forwarding as described [here](https://github.com/hse-aml/natural-language-processing/blob/master/AWS-tutorial.md#2-set-up-dependencies-and-run-your-project).

### How do I load data into Docker container?
To access the data in the container, we recommend to use `-v` flag described [here](#run-container-for-the-first-time) to mount a local directory from your computer into the container filesystem. For more details read [Docker documentation](https://docs.docker.com/storage/volumes/).

Alternatively, you can download data using Jupyter "Upload" button or `wget` command in the [Bash shell](#other-operations-on-the-container) of the container.

### Can't run `run_notebook` or `starspace` command
Make sure that you're executing it in the context of the Docker container as described [here](#run-container-for-the-first-time).

### "Name is already in use by container" when trying to run the container
This means that the container with this name is already created. You can connect to this container or remove it by following [instructions](#other-operations-on-the-container).

### StarSpace/Jupyter notebook crashes in Docker
This usually happens due to low default 2GB memory limit on Windows and OSX. Follow this [instructions](#change-ram-limits-of-the-container) to fix this.

### "This computer doesn't have VT-X/AMD-v enabled", when trying to run the container
This usually happens if you're using Docker Toolbox that needs Virtual Box support - hence the need for the hardware virtualization that can be enabled in BIOS.
Try to turn on the VT-X support in BIOS as described in [Microsoft documentation](https://blogs.technet.microsoft.com/canitpro/2015/09/08/step-by-step-enabling-hyper-v-for-use-on-windows-10/) or on [GitHub](https://github.com/docker/machine/issues/4271).

## Reporting the issue to the Coursera forum
Before reporting the issue to the Coursera forum, please, make sure that you've checked the [troubleshooting](#troubleshooting) steps. Only if they don't help, post all relevant error messages, throubleshooting results, and the following information to your post:

- Your operating system (e.g. Windows 7, Ubuntu Linux, OSX 10.13.3)
- Your docker version (e.g. Docker Toolbox, Docker for Windows, output of `docker --version`)
- Output of `docker ps -a`, `docker info`, `docker version -f "{{ .Server.Os }}"` (share thorough https://gist.github.com/ or https://pastebin.com/)
- Output of `wget http://localhost:8080` (or `wget http://192.168.99.100:8080` for Docker Toolbox), executed from within Docker container and outside of it

## Credits

The template for this dockerfile was taken from https://github.com/ZEMUSHKA/coursera-aml-docker
