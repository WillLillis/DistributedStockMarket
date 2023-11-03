# Running the program

## Running Locally (Non-Dockerized)

The three services can be started by running the following scripts in their respective ``order``, ``front-end``, and ``catalog`` directories. The order DOES matter when running the scripts, so please start with the catalog, then order, then frontend.

- ``start_order_service.sh``

- ``run_front-end_service.sh``

- ``run_catalog_service.sh``

Similarly, a client instance can be run by running the following command within the ``client`` directory. In ``<p>``'s place, one can specify the probability of the client sending an order request after receiving a positive response to a Lookup call.
``<p>`` must be in the range [0,1].

- ``FRONTEND_HOST=<front-end-machine-ip-address>
python3 client.py <p>``


### Testing Replicas

Our script for starting the order service puts three replicas of the service running in the background. To fully stop replicas at any time, we have an additional script that can be run:

- ``clean_by_port.sh <ports>``

Here ``<ports>`` can be a list of ports separated by spaces. Our order service replicas are running on ports 50054, 50055, and 50056. If one of the replicas are brought down, they can be brough up with a third script we have set up:

- ``restart_order_replica.sh``

By default, the restart replica script will restart the service on port 50054. If another port needs to be restarted, additional arguments need to be provided. An example for restarting port 50056 is as follows:

- ``./restart_order_replica.sh 50056 50054 50055``


## Dockerized Version

The dockerized version of the application can be run via the following commands in the lab's root directory:

- ``docker compose build``
- ``docker compose up``

Client instances run outside of the docker containers, as specified in the instructions above.

### Testing Replicas

Our order service replicas are named `order`, `order1`, and `order2`. To simulate a replica crashing and restarting, you can run the following commands in a separate terminal.

- ``docker-compose rm -s <order>``
- ``RESTART=1 docker compose up -d --build  <order>``

### Disabling cache

To test the dockerized application with cache disabled, first ensure the application is stopped with `docker-compose down`. Then run the following modified startup command.

- ``DISABLE_CACHE=1 docker compose up``

The application should run normally, just with the frontend cache disabled.

*The README.md containing the project instructions, our names, emails, and respective contributions is in the root directory of the project.*
*The steps to reproduce setting up the application on an AWS instance is detailed in aws_steps.md in the root directory of the project.*