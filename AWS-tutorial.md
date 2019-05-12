# Tutorial for setting up an AWS Virtual Machine

This tutorial will teach you how to set up an AWS Virtual Machine for the final project of our course. 

### 1. Register with AWS and launch an EC2 instance

First, you need to perform several preparatory steps (if you have already done this before, you can skip them):
- [Sign up for AWS](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#sign-up-for-aws). You will need to specify your credit card details, but for our project we will use Free Tier instances only, so you should not be charged.
- [Create a key pair for authentication](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#create-a-key-pair). If you use Windows, you will also need to install [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/) to use SSH.
- [Create security group](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#create-a-base-security-group). You must add rules to a security group to allow you to connect to your future instance from your IP address using SSH. You might want to allow SSH access from all IPv4 addresses (set to 0.0.0.0/0), because your IP might change.

Next, you are ready to create your first EC2 instance:
- [Launch a free tier instance](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance). For Amazon Machine Image (AMI) choose **Ubuntu Server 16.04 LTS**.
- [Connect to your instance](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-connect-to-instance-linux) using SSH.
- Later on you can [start and stop](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html) your instance when needed, and [terminate](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-clean-up-your-instance) it in the end.

### 2. Set up dependencies and run your project

- Install Docker container for Ubuntu with course dependencies. Follow our Docker instructions.

- To be able to access IPython notebooks running on AWS, you might want to SSH with port tunneling:
```sh
ssh -L 8080:localhost:8080 -i path/to/private_key ubuntu@ec2-XX-XXX-X-XX.us-east-2.compute.amazonaws.com
```
Then you will be able to see the notebooks on *localhost:8080* from your browser on the local machine.

If you're using PuTTY, before you start your SSH connection, go to the PuTTY Tunnels panel. Make sure the «Local» and «Auto» radio buttons are set. Enter the local port 8080 number into the «Source port» box. Enter the destination host name and port number into the «Destination» box, separated by a colon ubuntu@ec2-XX-XXX-X-XX.us-east-2.compute.amazonaws.com:8080.
For more details see [this guide](https://www.akadia.com/services/ssh_putty.html).

- Bring code and data to AWS instance, e.g.
```sh
scp -i path/to/your_key.pem path/to/local_file ubuntu@ec2-XX-XXX-X-XX.us-east-2.compute.amazonaws.com:path/to/remote_file
``` 
You might need to install [WinSCP](https://winscp.net/eng/docs/lang:ru) for data transfer if you are using Windows.

- It is also a good practice to use [tmux](https://medium.com/@peterxjang/a-minimalist-guide-to-tmux-13675fb160fa) to keep your remote session running even if you disconnect from the machine, e.g. by closing your laptop. 

Thus, to run your scipts on the machine, we suggest that you run:  ssh -> tmux -> docker -> python.
