
# How to run Our Stock Service on AWS

I'll describe below, step by step, exactly how we got our service running on an aws ec2 ``t2.micro`` instance.
A fair amount of this will be a repeat of the Lablet 5 instructions.

-  Log into canvas and access the "Learner Lab" Module
	
	- Select "Start Lab"

	- After the lab has started, select "AWS Details"

	- Copy the resulting text into ``~/.aws/credentials``

	- Click the ``Download PEM`` button and save it to your working directory

	- Run ``aws configure``
		
		1. It will ask your AWS Access Key ID, we have already configured that in the previous step by
		   creating a credentials file. Just press enter to skip this step.
		2. It will ask your AWS Secret Access Key, we have also configured that in the previous step. Press
		   enter to skip this step.
		3. For default region name, be sure to input `us-east-1`. Otherwise the PEM key we just downloaded
		   won't work!
		4. For default output format, input `json`.

- Start an instance by running ``aws ec2 run-instances --image-id ami-0d73480446600f555 --instance-type t2.micro --key-name vockey > instance.json``

	- Find the ``InstanceId`` field via ``cat instance.json | grep InstanceId``

	- Check to make sure the instance is running via ``aws ec2 describe-instances --instance-id <your-instance-id>``

- Run ``chmod 400 labuser.pem``

- Authorize the necessary ports for our service to work by running ``aws ec2 authorize-security-group-ingress --group-name default --protocol tcp --port <port-number> --cidr 0.0.0.0/0``
	
	- Run the command with ``<port-number> = 22, 5000, 50053, 50054, 50055,`` and ``50056``.

- Find the instance's public DNS name via ``aws ec2 describe-instances --instance-id <your-instance-id> | grep PublicDnsName``

- SSH into the instance via ``ssh -i labuser.pem ubuntu@<public-DNS-name>``
	
	- Enter ``yes`` if prompted

- Now we have to install a bunch of stuff in order for our program to run:

	- ``sudo apt-get update``

	- ``sudo apt-get install docker.io -y``

		- Verify the install by running ``docker --version``
	
	- ``sudo service docker start``

	- ``sudo apt-get install curl -y``

	- ``DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}``

	- ``mkdir -p $DOCKER_CONFIG/cli-plugins``

	- ``curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose``

	- ``chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose``

		- Verify the install by running ``docker compose version``

	- ``sudo apt-get install git``

	- Next we created a key on our instance to allow us to clone our github repository

		- ``ssh-keygen``

			- Hit enter to specify default arguments for all prompts

		- ``cat ~/.ssh/id_rsa.pub``

		- Copy the output, and add it to github as an ``ssh`` key

			- Access the github profile of a contributor to the repo

			- Access Settings->SSH and GPG Keys->New SSH key

			- Paste your copied key into the textbox

	- Run ``git clone git@github.com:umass-cs677-current/spring23-lab-3-pshekar-and-wlillis.git`` to clone the repository

	- Change into the project's working directory, ``spring23-lab-3-pshekar-and-wlillis``

- ``sudo docker compose build``

- ``sudo docker compose up``

- Run the client locally to test the service however you would like.

	- The client can optionally be run via the ``run_client.sh`` script.
		
		- The first argument is the public DNS of the aws instance

		- The second argument is the probability ``p`` of making an order following a lookup. Leaving this blank will run ``client.py`` with ``p=1``.

	- To kill an order replica, run ``docker-compose rm -s <order-container>``, where ``<order-container>= order, order1, `` or ``order2``.
	
	- to restart a crashed order replica, run ``RESTART=1 docker-compose up -d --build  <order-container>``, again where ``<order-container>= order, order1, `` or ``order2``.
